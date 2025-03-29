import threading
import time
import random
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Dummy In-Memory Vector Store ---
# In production, this would be replaced by Pathway’s dynamic vector store.
vector_store = []

# --- Data Ingestion: Simulate Real-Time Transaction Data ---
def ingest_transactions():
    """
    Simulate real-time ingestion of transaction data.
    In a real implementation, connect to financial APIs/webhooks here.
    """
    while True:
        transaction = {
            "timestamp": time.time(),
            "amount": round(random.uniform(10, 100), 2),
            "merchant": random.choice(["Store A", "Store B", "Store C"]),
            "category": random.choice(["Food", "Transport", "Shopping"])
        }
        vector_store.append(transaction)
        st.write(f"New transaction ingested: {transaction}")
        # In production, immediately update Pathway's vector store here.
        time.sleep(10)  # simulate a new transaction every 10 seconds

# --- Context Retrieval: Dummy Function ---
def retrieve_context(query):
    """
    Simulate retrieval from a vector store.
    Replace with actual queries against Pathway's vector store.
    """
    # For demonstration, return the last 5 transactions.
    return vector_store[-5:] if len(vector_store) >= 5 else vector_store

# --- Fetch AI Agent Logic (Dummy RAG Implementation) ---
def process_query(query):
    """
    Simulate processing a natural language query using RAG.
    This function retrieves context and performs a simple calculation.
    """
    context = retrieve_context(query)
    total_spent = sum(tx["amount"] for tx in context)
    response = (
        f"Based on your last {len(context)} transactions, "
        f"you have spent a total of ${total_spent:.2f}. "
        "You may afford a $50 purchase if your remaining budget allows."
    )
    return response, context

# --- Start Data Ingestion in Background ---
# We use Streamlit's session_state to ensure the background thread starts only once.
if "ingestion_started" not in st.session_state:
    ingestion_thread = threading.Thread(target=ingest_transactions, daemon=True)
    ingestion_thread.start()
    st.session_state.ingestion_started = True

# --- Streamlit App UI ---
st.title("Real-Time Personal Finance Tracker")

# Section: Query Input & Response
st.header("Ask a Financial Question")
query_input = st.text_input("Enter your query (e.g., 'Can I afford a $50 purchase?'):")

if st.button("Submit Query"):
    if query_input:
        response_text, context = process_query(query_input)
        st.success(response_text)
        st.write("Context (Recent Transactions):")
        st.write(pd.DataFrame(context))
    else:
        st.warning("Please enter a query.")

# Section: Date-Based Expenditure Breakdown (Static Example)
st.header("Expenditure Breakdown")
# In a real implementation, fetch and aggregate day-wise data from the vector store.
# Here, we simulate day-wise data.
chart_data = {
    "date": ["2025-03-25", "2025-03-26", "2025-03-27"],
    "expenditure": [120.50, 85.00, 150.75]
}
df_chart = pd.DataFrame(chart_data)
fig = px.bar(df_chart, x="date", y="expenditure", title="Day-wise Expenditures")
st.plotly_chart(fig)

# Optionally, add interactive elements to the chart:
st.markdown(
    """
    **Note:** Click on a bar in the chart above to view detailed spending information.
    (Interactive drill-down functionality can be implemented with additional callbacks.)
    """
)
