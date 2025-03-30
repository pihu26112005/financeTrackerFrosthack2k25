import streamlit as st

def main():
    st.title("File Upload App")
    
    if st.button("Add File"):
        st.write("Button clicked!")

if __name__ == "__main__":
    main()
