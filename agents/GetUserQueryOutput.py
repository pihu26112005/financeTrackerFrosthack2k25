import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pathwayF.langchainPathwayClient import run



load_dotenv(find_dotenv())
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'advanced-rag'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


def answerQuery(user_query, filtered_transactions):
    # with open("INFO/filtered_transactions.json", "r") as file:
    #     filtered_transactions = json.load(file)
        

    # user_query = "what i did in march this year betweeen 3rd and 5th"
    # ans = run(user_query)

    transactions_context = json.dumps(filtered_transactions, indent=4)

    prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are analyzing a list of financial transactions. Each transaction contains Date, Particulars, Deposit, Withdrawal, and Balance. "
               "Answer the user's question based on the given transactions. Respond accurately based only on the provided data."),
    ("user", "Transactions Data:\n{transactions}\n\nUser Query: {query}"),
    # ("assistant", "This is output from a separate summarizing agent. You are supposed to only take contextual input from this agent. DO NOT OVERWRITE factual data from this to that of system. - {ans}")
    ])



    model = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  
        temperature=0.7,
        max_length=200
        )

#     model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )

    prompt = prompt_template.format(transactions=transactions_context, query=user_query)
    response = model.invoke(prompt)

    # Print the response
    print("LLM Response:", response)
    return response
