import streamlit as st
import requests

def main():
    st.title("File Upload App")
    
    if st.button("Add File"):
        response = requests.get("http://0.0.0.0:8000/rest/get")
        st.write(response.json())
        st.write("Button clicked!")

    query = st.text_input("Enter your query")
    if st.button("Get Relevant Transactions"):
        if query:  # Ensure query is not empty
            response = requests.post(f"http://0.0.0.0:8000/rest/post", json={"message": query})
            st.write(response.json())
        else:
            st.warning("Please enter a query before clicking the button.")

    if st.button("Get Ansswer"):
        if query:  # Ensure query is not empty
            # response = requests.get(f"http://127.0.0.1:8001/AnswerQuery", params={"qury": query})
            response = requests.post(f"http://0.0.0.0:8000/pest/post", json={"message": query})
            st.write(response.json())
        else:
            st.warning("Please enter a query before clicking the button.")

if __name__ == "__main__":
    main()
