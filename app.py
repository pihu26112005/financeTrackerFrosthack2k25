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

def main():
    """Main function to handle page selection"""
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a Page", ["Upload File", "Query Transactions"])

    if page == "Upload File":
        upload_page()
    elif page == "Query Transactions":
        query_page()

if __name__ == "__main__":
    main()
