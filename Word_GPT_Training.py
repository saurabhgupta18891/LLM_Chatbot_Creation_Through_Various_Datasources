# # import docx
# #
# # def extract_text_from_word_document(file_path):
# #     doc = docx.Document(file_path)
# #     text = ""
# #
# #     for paragraph in doc.paragraphs:
# #         text += paragraph.text + "\n"
# #
# #     return text
# #
# # # if __name__ == "__main__":
# #     # Path to your Word document
# # doc_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\SAURABH_GUPTA_CV (5).docx"
# #
# # # Extract text from the Word document
# # extracted_text = extract_text_from_word_document(doc_path)
# #
# # # Print the extracted text
# # print(extracted_text)
# import os
# from langchain.document_loaders import DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# import pinecone
# from langchain.vectorstores import Pinecone
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
#
# os.environ["OPENAI_API_KEY"] = "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"
#
# directory = r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Doc_Files'
#
# def load_docs(directory):
#   loader = DirectoryLoader(directory)
#   documents = loader.load()
#   return documents
#
# documents = load_docs(directory)
# #len(documents)
# print(documents)
#
#
#
# def split_docs(documents,chunk_size=1000,chunk_overlap=20):
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#   docs = text_splitter.split_documents(documents)
#   return docs
#
# docs = split_docs(documents)
# print(len(docs))
#
# import openai
#
#
# embeddings = OpenAIEmbeddings(model_name="ada")
#
# # query_result = embeddings.embed_query("Hello world")
# # len(query_result)
#
#
# # initialize pinecone
# pinecone.init(
#     api_key="50a56383-a02e-4827-a94f-51c02199045e",  # find at app.pinecone.io
#     environment="gcp-starter"  # next to api key in console
# )
# index_name = "langchain-demo"
# #pinecone.create_index(index_name, dimension=1536)
#
# index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
#
# def get_similar_docs(query,index,k=2,score=False):
#   if score:
#     similar_docs = index.similarity_search_with_score(query,k=k)
#   else:
#     similar_docs = index.similarity_search(query,k=k)
#   return similar_docs
#
# #query = "Who is Saurabh Gupta?"
# query="what is the contact no of Saurabh Gupta?"
# similar_docs = get_similar_docs(query,index)
# print(similar_docs)
#
#
#
#
#
# def get_answer(query):
#   similar_docs = get_similar_docs(query,index)
#   model_name = "text-davinci-003"
#   #model_name = "gpt-3.5-turbo"
#   # model_name = "gpt-4"
#   llm = OpenAI(model_name=model_name)
#   #llm = ChatOpenAI(model_name=model_name)
#
#   chain = load_qa_chain(llm, chain_type="stuff")
#   # print(similar_docs)
#   answer =  chain.run(input_documents=similar_docs, question=query)
#   return  answer
#
# #query = "Who is Saurabh Gupta?"
# answer=get_answer(query)
# print(answer)
# #
# #
# #
# #
# #
# # ########
# #
# # def get_answer_from_word_file(word_file_path, user_query):
# #   # Load the Word file and extract text
# #   documents = load_docs(word_file_path)
# #
# #   # Get similar documents based on the user query
# #   similar_docs = get_similar_docs(user_query)
# #
# #   # Run the question-answering chain to get the answer
# #   answer = get_answer(user_query)
# #
# #   return answer
# #
# #
# # # Example usage
# # word_file_path = "path_to_your_word_file.docx"  # Replace with the actual path to your Word file
# # user_query = "What is the main topic of the document?"
# #
# # answer = get_answer_from_word_file(word_file_path, user_query)
# # print("Answer:", answer)
#
#
#
#
# ###
# #
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import shutil

os.environ["OPENAI_API_KEY"] = "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"
YOUR_PINECONE_API_KEY="50a56383-a02e-4827-a94f-51c02199045e"


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


