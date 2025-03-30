import streamlit as st
import requests
import os
import plotly.express as px
import pandas as pd
import json

# Create the directory if it doesn't exist
DATA_DIR = "INFO/data"
os.makedirs(DATA_DIR, exist_ok=True)

def upload_page():
    """Page for uploading a file & viewing transaction graphs"""
    st.title("📂 Upload & View Transactions")

    ### 🔹 Section 1: Upload Feature
    st.header("🚀 Upload File")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        file_path = os.path.join(DATA_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File '{uploaded_file.name}' saved successfully!")

        # Store filename in session state
        st.session_state["uploaded_filename"] = uploaded_file.name

    if st.button("🔄 Add File Data"):
        if "uploaded_filename" in st.session_state:
            response = requests.post(
                "http://0.0.0.0:8000/nest/post",
                json={"message": st.session_state["uploaded_filename"]}
            )
            st.write(response.json())
            st.write("📌 Button clicked!")
        else:
            st.warning("⚠️ Please upload a file before clicking 'Add File Data'.")

    ### 🔹 Section 2: Show Graphs for Transactions
    st.header("📊 Transaction Analytics")

    json_path = "INFO/processed_output.json"

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)  # Load JSON file

        # Show dropdown to select a file (Month)
        pdf_names = list(data.keys())
        selected_pdf = st.selectbox("📅 Select a Month:", pdf_names)

        if selected_pdf in data:
            transactions = data[selected_pdf]  # Get transactions for selected PDF

            if transactions:
                df = pd.DataFrame(transactions)  # Convert to DataFrame
                df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

                # Show Raw Data
                st.subheader("📜 Transaction Data")
                st.dataframe(df)

                # 1️⃣ Line Chart: Balance Over Time
                st.subheader("📈 Balance Over Time")
                fig_balance = px.line(df, x="Date", y="Balance", title="Balance Trend", markers=True)
                st.plotly_chart(fig_balance)

                # 2️⃣ Bar Chart: Deposit vs Withdrawal
                st.subheader("💰 Deposit vs Withdrawal")
                df["Deposit"] = df["Deposit"].fillna(0)
                df["Withdrawal"] = df["Withdrawal"].fillna(0)

                fig_bar = px.bar(df, x="Date", y=["Deposit", "Withdrawal"], 
                                 title="Deposits & Withdrawals", 
                                 barmode="group")
                st.plotly_chart(fig_bar)

                # 3️⃣ Area Chart: Cumulative Deposits & Withdrawals
                st.subheader("📊 Cumulative Deposits & Withdrawals")
                df["Cumulative Deposit"] = df["Deposit"].cumsum()
                df["Cumulative Withdrawal"] = df["Withdrawal"].cumsum()

                fig_area = px.area(df, x="Date", y=["Cumulative Deposit", "Cumulative Withdrawal"],
                                   title="Cumulative Deposits vs Withdrawals")
                st.plotly_chart(fig_area)

                # 4️⃣ Histogram: Transactions Per Day
                st.subheader("📊 Daily Transaction Count")
                df["Transaction Count"] = 1  

                fig_hist = px.histogram(df, x="Date", y="Transaction Count", 
                                        title="Transactions Per Day", nbins=len(df["Date"].unique()))
                st.plotly_chart(fig_hist)

            else:
                st.warning(f"⚠️ No transactions found for '{selected_pdf}'.")
    else:
        st.warning("⚠️ Processed transaction data not found!")


def query_page():
    """Page for querying transactions"""
    st.title("🔍 Query Transactions")

    query = st.text_input("🔎 Enter your query")

    if st.button("📌 Get Relevant Transactions"):
        if query:
            response = requests.post("http://0.0.0.0:8000/rest/post", json={"message": query})
            data = response.json()

            if "fld" in data and isinstance(data["fld"], list) and len(data["fld"]) > 0:
                transactions = data["fld"]
                
                # Convert to DataFrame
                df = pd.DataFrame(transactions)
                df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

                # Show transactions in table format
                st.subheader("📜 Query Results")
                st.dataframe(df)

                # Line Chart: Balance Over Time
                st.subheader("📈 Balance Trend")
                fig_balance = px.line(df, x="Date", y="Balance", title="Balance Trend", markers=True)
                st.plotly_chart(fig_balance)

            else:
                st.warning("⚠️ No transactions found for your query!")

        else:
            st.warning("⚠️ Please enter a query before clicking the button.")

    # if st.button("Get Answer"):
    #     if query:
    #         response = requests.post("http://0.0.0.0:8000/pest/post", json={"message": query})
    #         st.write(response.json())
    #     else:
    #         st.warning("Please enter a query before clicking the button.")

def chat_page():
    """Page for chatting with the model"""
    st.title("chat with model")

    query = st.text_input("Enter your query")

    if st.button("Get Answer"):
        if query:
            response00 = requests.post("http://0.0.0.0:8000//context/post", json={"message": query})
            # st.write(response00.json())
            answer = response00.json().get("ans")
            if(answer.lower() == "yes"):
                response0 = requests.post("http://0.0.0.0:8000/rest/post", json={"message": query})
                response = requests.post("http://0.0.0.0:8000/pest/post", json={"message": query})
                response2 = requests.post("http://0.0.0.0:8000/query", json={"message": query})
                st.write(response2.json())
                st.write(response.json())
            else:
                st.write(answer)
        else:
            st.warning("Please enter a query before clicking the button.")

    # if st.button("Get vector answer"):
    #     if query:
    #         response = requests.post("http://0.0.0.0:8000/query", json={"message": query})
    #         st.write(response.json())
    #     else:
    #         st.warning("Please enter a query before clicking the button.")
    

def search_page():
    """New Page for Searching"""
    st.header("🔍 Search Transactions")

    key = st.text_input("📂 Key / Month (e.g., mar_2025.pdf)")
    start_date = st.text_input("📅 Start Date (DD-MM-YYYY)")
    end_date = st.text_input("📅 End Date (DD-MM-YYYY)")

    if st.button("🚀 Search"):
        if key and start_date and end_date:
            response = requests.post(
                "http://0.0.0.0:8000/search", 
                json={"key": key, "start_date": start_date, "end_date": end_date}
            )
            data = response.json()  

            # Extract transactions from "filtered_transactions" key
            transactions = data.get("filtered_transactions", [])

            if isinstance(transactions, list) and len(transactions) > 0:
                df = pd.DataFrame(transactions)  # Convert JSON to DataFrame
                
                # Convert 'Date' to datetime for plotting
                df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

                # Show raw data
                st.subheader("📊 Raw Transaction Data")
                st.dataframe(df)

                # 1️⃣ Line Chart: Account Balance Over Time
                st.subheader("📈 Balance Over Time")
                fig_balance = px.line(df, x="Date", y="Balance", title="Balance Trend", markers=True)
                st.plotly_chart(fig_balance)

                # 2️⃣ Bar Chart: Deposit vs Withdrawal
                st.subheader("💰 Deposit vs Withdrawal")
                df["Deposit"] = df["Deposit"].fillna(0)  # Handle NaN values
                df["Withdrawal"] = df["Withdrawal"].fillna(0)

                fig_bar = px.bar(df, x="Date", y=["Deposit", "Withdrawal"], 
                                 title="Deposits & Withdrawals", 
                                 barmode="group")
                st.plotly_chart(fig_bar)

                # 3️⃣ Area Chart: Cumulative Deposits & Withdrawals
                st.subheader("📊 Cumulative Deposits & Withdrawals")
                df["Cumulative Deposit"] = df["Deposit"].cumsum()
                df["Cumulative Withdrawal"] = df["Withdrawal"].cumsum()

                fig_area = px.area(df, x="Date", y=["Cumulative Deposit", "Cumulative Withdrawal"],
                                   title="Cumulative Deposits vs Withdrawals")
                st.plotly_chart(fig_area)

                # 4️⃣ Histogram: Transactions Per Day
                st.subheader("📊 Daily Transaction Count")
                df["Transaction Count"] = 1  # Each row is a transaction

                fig_hist = px.histogram(df, x="Date", y="Transaction Count", 
                                        title="Transactions Per Day", nbins=len(df["Date"].unique()))
                st.plotly_chart(fig_hist)

            else:
                st.warning("⚠️ No transactions found for the given inputs.")
        else:
            st.warning("⚠️ Please fill in all fields before searching.")

def main():
    """Main function to handle navigation with sidebar"""
    st.sidebar.title("🔗 Navigation")
    page = st.sidebar.radio("Go to", ["📂 Upload File", "🔎 Query Transactions","💬 Chat" ,"🔍 Search"])

    if page == "📂 Upload File":
        upload_page()
    elif page == "🔎 Query Transactions":
        query_page()
    elif page == "🔍 Search":
        search_page()
    elif page == "💬 Chat":
        chat_page()


if __name__ == "__main__":
    main()