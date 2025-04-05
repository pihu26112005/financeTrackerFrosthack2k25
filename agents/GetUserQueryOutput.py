import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pathwayF.langchainPathwayClient import run
from asi_chat import llmChat



load_dotenv(find_dotenv())
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'advanced-rag'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


def answerQuery(user_query, filtered_transactions):
    ans = run(user_query)

    transactions_context = json.dumps(filtered_transactions, indent=4)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are analyzing a list of financial transactions. Each transaction contains Date, Particulars, Deposit, Withdrawal, and Balance. "
                "Answer the user's question based on the given transactions. Respond accurately based only on the provided data."),
        ("assistant", "Below is the output from a separate summarizing agent providing relevant contextual background. Please use this information only as a guide to enhance your final answer. Do not extract or override any factual details provided in the system message; integrate only the pertinent context to refine your response. - {ans}"),
        ("user", "Transactions Data:\n{transactions}\n\nUser Query: {query}"),
    ])


    prompt = prompt_template.format_messages(transactions=transactions_context, query=user_query)
    # response = model.invoke(prompt)
    response = llmChat(prompt)

    # Print the response
    print("LLM Response:", response)
    return response
