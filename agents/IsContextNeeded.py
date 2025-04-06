import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from asi_chat import llmChat


load_dotenv(find_dotenv())
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'advanced-rag'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


def CheckQuery(query):
    # Step 1: Ask if searching the financial database is needed
    check_prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an AI assistant responsible for determining whether a user's query requires searching their financial transaction database.\n\n"
     "**Rules for Answering:**\n"
     "- If the query contains any greeting (e.g., 'Hi', 'Hello', 'How are you?', 'Good morning', etc.), respond with **'No'**.\n"
     "- If the query asks about transactions, balances, deposits, withdrawals, dates, or any financial information, respond with **'Yes'**.\n"
     "- Do not explain or provide any extra text—strictly return only 'Yes' or 'No'.\n"
     "- If unsure, assume the safest answer is 'Yes'.\n\n"
     "**Response Format:**\n"
     "- Reply with exactly one word: **Yes** or **No** (case-insensitive).\n"
     "- No punctuation, no explanations, no formatting—only a single word response."
    ),
    ("user", "User Query: {query}")
]   )

    # model = HuggingFaceEndpoint(
    #     repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  
    #     temperature=0.7,
    #     max_length=200
    # )
#     model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )

    check_prompt = check_prompt_template.format_messages(query=query)
    response = llmChat(check_prompt)
    # response = model.invoke(check_prompt) # Clean up response

    print("LLM Response:", response)  # Debugging
    print("LLM Response:", response)  # Debugging

    match = re.search(r'\b(Yes|No)\b', response, re.IGNORECASE)
    extracted_answer = match.group(1).lower() if match else "no" 

    print("Extracted Answer:", extracted_answer)  # Debugging

    if extracted_answer.lower() == "yes":
        return "Yes"

    # Step 2: If "No", ask the model to answer the query directly
    answer_prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Answer user query in one or two line"),
        ("user", "User Query: {query}")
    ])

    answer_prompt = answer_prompt_template.format_messages(query=query)
    # final_response = model.invoke(answer_prompt)
    final_response = llmChat(answer_prompt)  # Clean up response
    print("Final Response:", final_response)  # Debugging

    return final_response  # Return the actual answer
