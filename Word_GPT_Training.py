import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import shutil

os.environ["OPENAI_API_KEY"] = ""
YOUR_PINECONE_API_KEY=""


def save_word_file_to_directory(file):
    # Create the directory if it doesn't exist
    directory = "input_word_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the file name from the original path
    file_name = os.path.basename(file)

    # Define the new file path in the desired directory
    new_file_path = os.path.join(directory, file_name)

    # Copy the existing Word document to the directory
    shutil.copy(file, new_file_path)

    return directory

# Example usage
input_word_file_path = "SAURABH_GUPTA_CV (5).docx"  # Replace with the actual path to the existing Word file

# Save the existing Word file to the directory
# saved_file_path = save_word_file_to_directory(input_word_file_path)
# print("Word file saved at:", saved_file_path)


def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

def initialize_pinecone_and_create_index(api_key, index_name, docs, embeddings):
  # Initialize Pinecone
  pinecone.init(api_key=api_key,environment="gcp-starter")

  # Create the index
  pinecone.create_index(index_name, dimension=1536)

  # Create a Pinecone index and add the documents
  index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

  return index

def get_similar_docs(query,index,k=2,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

def get_answer(query,similar_docs):
  model_name = "text-davinci-003"
  # model_name = "gpt-3.5-turbo"
  # model_name = "gpt-4"
  llm = OpenAI(model_name=model_name)

  chain = load_qa_chain(llm, chain_type="stuff")
  # print(similar_docs)
  answer =  chain.run(input_documents=similar_docs, question=query)
  return  answer


def get_answer_from_word_file(input_word_file_path, user_query):
  # Load the Word file and extract text using load_docs
  new_directory_path=save_word_file_to_directory(input_word_file_path)
  print(new_directory_path)

  documents = load_docs(new_directory_path)
  print(documents)

  docs=split_docs(documents, chunk_size=1000, chunk_overlap=20)
  print(docs)
  # Initialize Pinecone and create the index
  index_name = "langchain-demo"
  embeddings = OpenAIEmbeddings(model_name="ada")
  index = initialize_pinecone_and_create_index(YOUR_PINECONE_API_KEY, index_name, docs, embeddings)
  print(index)
  # Get similar documents based on the user query
  similar_docs = get_similar_docs(user_query,index,k=2,score=False)

  # Run the question-answering chain to get the answer
  answer = get_answer(user_query,similar_docs)

  return answer


# Example usage
# word_file_path = "path_to_your_word_file.docx"  # Replace with the actual path to your Word file
# user_query = "What is the main topic of the document?"
# word_file_path = r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Doc_Files'
user_query="what is the contact no of saurabh gupta?"

answer = get_answer_from_word_file(input_word_file_path, user_query)
print("Answer:", answer)


