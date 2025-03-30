import streamlit as st
import json
import requests

def main():
    st.title("File Upload App")
    
    if st.button("Add File"):
        response = requests.get("http://127.0.0.1:8001/CreateDatabase")
        st.write(response.json())
        st.write("Button clicked!")

if __name__ == "__main__":
    main()
