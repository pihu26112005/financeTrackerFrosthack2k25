import os
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import json


def process_pdfs(data_folder):
    """Process all PDFs in the given folder and store extracted text in a dictionary."""
    pdf_text_data = {}
    
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_folder, filename)
            
            # Load PDF using LangChain's PyPDFLoader
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Extract text from each page
            pages_text = [page.page_content for page in pages]
            
            # Use LangChain's CharacterTextSplitter if needed
            splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
            split_pages_text = [splitter.split_text(page) for page in pages_text]
            
            pdf_text_data[filename] = split_pages_text
    
    return pdf_text_data

if __name__ == "__main__":
    data_folder = "INFO/data"
    result = process_pdfs(data_folder)
    
    # Save output to a JSON file
    with open("INFO/output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print("Processing complete. Extracted text saved to output.json.")
