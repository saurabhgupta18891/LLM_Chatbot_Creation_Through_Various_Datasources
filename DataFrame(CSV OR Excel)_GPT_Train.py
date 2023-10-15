from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
import os
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent

app = Flask(__name__)

# Load CSV data and create a Pandas agent
os.environ["OPENAI_API_KEY"] = ""
# output_csv = r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\excel_file_example.csv'
# df = pd.read_csv(output_csv)
# pd_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=False)

# Define an API endpoint to handle user queries
@app.route('/', methods=['GET','POST'])
def ask_question():
    # Get user query from request
    user_query = request.form.get('user_query')
    #uploaded_file = request.files['file']

    #df = pd.read_csv(uploaded_file,encoding="utf-8")
    output_csv = r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\excel_file_example.csv'
    df = pd.read_csv(output_csv)
    pd_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=False)

    # Use the Pandas agent to get the answer
    answer = pd_agent.run(user_query)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000,debug=True)
