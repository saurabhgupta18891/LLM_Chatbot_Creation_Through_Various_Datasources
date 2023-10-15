# Chatbot Creation using various Data Sources
# Description

In the given project I am solving a problem of LLM(GPT) Model Training using various data sources like Documents(PDF, Word), speech, Audio, etc.

I have experimented with and implemented various methods to achieve my goal.

1. For the Speech part I used AWS Transcribe and GCP Speech to Text services and for the multilingual audio files I created a function that will return transcripted text from the input audio file and then that text will be used to train the GPT model.
  
2. For the Docs part I used langchain modules to load the text data from docs and then train it using GPT.

3. For the tabular(data frame) type of data I used langchain pandas data frame agent to answer the queries of users.(refer DataFrame(CSV OR Excel)_GPT_Train.py)

4. For the conversation part langchain chains are used for smooth chatting between the user and bot

5. Pinecone Vectordatabase has been used to store the vectors and when the user asks a query the response is generated using similarity search. (refer Word_GPT_Training.py)

For an overall application, one API will incorporate all the functions based on the requirements of the user the API will respond accordingly. it will train the model and then give answers to the user's questions.
