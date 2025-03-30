import streamlit as st
import requests
import os

# Create the directory if it doesn't exist
DATA_DIR = "INFO/data"
os.makedirs(DATA_DIR, exist_ok=True)

def upload_page():
    """Page for uploading a file"""
    st.title("Upload File")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    if uploaded_file:
        file_path = os.path.join(DATA_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' saved successfully!")

        # Store the filename in session state for later use
        st.session_state["uploaded_filename"] = uploaded_file.name

    if st.button("Add File Data"):  # API call with file name
        if "uploaded_filename" in st.session_state:
            response = requests.post(
                "http://0.0.0.0:8000/nest/post",
                json={"message": st.session_state["uploaded_filename"]}
            )
            st.write(response.json())
            st.write("Button clicked!")
        else:
            st.warning("Please upload a file before clicking 'Add File Data'.")


def query_page():
    """Page for querying transactions"""
    st.title("Query Transactions")

    query = st.text_input("Enter your query")

    if st.button("Get Relevant Transactions"):
        if query:
            response = requests.post("http://0.0.0.0:8000/rest/post", json={"message": query})
            st.write(response.json())
        else:
            st.warning("Please enter a query before clicking the button.")

    if st.button("Get Answer"):
        if query:
            response = requests.post("http://0.0.0.0:8000/pest/post", json={"message": query})
            st.write(response.json())
        else:
            st.warning("Please enter a query before clicking the button.")

def search_page():
    """New Page for Searching"""
    st.header("🔍 Search Transactions")

    key = st.text_input("📂 Key / Month (e.g., mar_2023.pdf)")
    start_date = st.text_input("📅 Start Date (DD-MM-YYYY)")
    end_date = st.text_input("📅 End Date (DD-MM-YYYY)")

    if st.button("🚀 Search"):
        if key and start_date and end_date:
            response = requests.post(
                "http://0.0.0.0:8000/search", 
                json={"key": key, "start_date": start_date, "end_date": end_date}
            )
            st.json(response.json())  # Display formatted JSON output
        else:
            st.warning("⚠️ Please fill in all fields before searching.")

def main():
    """Main function to handle navigation with sidebar"""
    st.sidebar.title("🔗 Navigation")
    page = st.sidebar.radio("Go to", ["📂 Upload File", "🔎 Query Transactions", "🔍 Search"])

    if page == "📂 Upload File":
        upload_page()
    elif page == "🔎 Query Transactions":
        query_page()
    elif page == "🔍 Search":
        search_page()

if __name__ == "__main__":
    main()