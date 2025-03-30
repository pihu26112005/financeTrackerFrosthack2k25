from typing import Literal, Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv, find_dotenv
import os
import json
import re
from datetime import datetime



load_dotenv(find_dotenv())
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'advanced-rag'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")


# Function to get relevant transactions based on user query
def get_relevance(user_query: str) -> List[str]:
    """
    Filters transactions based on user query and returns a list containing:
    [relevant key, initial date, final date]
    """
    prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You have a dictionary containing transactions grouped by months. Keys are in the format 'jan_2025.pdf', 'feb_2025.pdf', etc. "
     "Remeber Current YEar is 2025.\n\n"
     "Each key represents a PDF file corresponding to a specific month and year. The values are lists of transactions, each having the fields: "
     "'Date', 'Particulars', 'Deposit', 'Withdrawal', and 'Balance'.\n\n"
     "Example of a transaction:\n"
     "{{\n"
     '    "Date": "01-02-2025",\n'
     '    "Particulars": "UPI/DR/503291190852/PIYUSH KU/PPIW/**86231@FAM/UPI//S BIA261AE17B77646879B30D18 8C204C9B6/01/02/2025 12:49:21",\n'
     '    "Deposit": 100.0,\n'
     '    "Withdrawal": null,\n'
     '    "Balance": 13913.0\n'
     "}}\n\n"
     "Instructions:\n"
     "- Identify the relevant month and year from the user query and return only the matching key (e.g., 'jan_2025.pdf').\n"
     "- Infer the date(s) based on the user's query and return them in the format **DD-MM-YYYY**.\n"
     "- The response must be **strictly** in JSON format with only the required key and date range.\n"
     "- The output must contain **nothing else**—no explanations, headers, or extra text.\n\n"
     "Format the output as:\n"
     "{{\n"
     '    "key": "<matching_file_name>.pdf",\n'
     '    "date_range": {{"start": "<earliest_date>", "end": "<latest_date>"}}\n'
     "}}"
    ),
    ("user", "User query: {query}")
    ])



    
    # model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    model = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  # ✅ Correct model
    temperature=0.7,
    max_length=200
    )
    
    prompt = prompt_template.format(query=user_query)
    response = model.invoke(prompt)
    
    return response

# Example usage
# user_query = "what i did in march this year betweeen 3rd and 5th"
# result = get_relevance(user_query)
# print("Raw result:", result[8:-1])
# print("Type of result:", type(result))

# def get_relevant_transactions(user_query: str):
    # result = get_relevance(user_query)
def get_relevant_transactions(result,database):
    match = re.search(r'\{.*\}', result, re.DOTALL)  # Find JSON inside curly brackets
    parsed_result = None
    if match:
        clean_json = match.group(0)  # Extract JSON string
        parsed_result = json.loads(clean_json)  # Parse it
        # print("Parsed JSON:", parsed_result)
    else:
        raise ValueError("No valid JSON found in result")

    # with open("INFO/processed_output.json", "r") as file:
    #     database = json.load(file)

    key = parsed_result["key"]  # Example: "mar_2023.pdf"
    start_date = parsed_result["date_range"]["start"]  # Example: "03-03-2023"
    end_date = parsed_result["date_range"]["end"]  # Example: "05-03-2023"

    start_dt = datetime.strptime(start_date, "%d-%m-%Y")
    end_dt = datetime.strptime(end_date, "%d-%m-%Y")

    if key in database:
        transactions = database[key]  

        filtered_transactions = [
            txn for txn in transactions
            if start_dt <= datetime.strptime(txn["Date"], "%d-%m-%Y") <= end_dt
        ]
        # print("Filtered Transactions:", json.dumps(filtered_transactions, indent=4))
        return filtered_transactions
        # return json.dumps(filtered_transactions, indent=4)
    
        # output_file = "INFO/filtered_transactions.json"
        # with open(output_file, "w") as file:
        #     json.dump(filtered_transactions, file, indent=4)
        # print(f"Filtered transactions saved to {output_file}")
        
    else:
        print(f"No transactions found for {key}")