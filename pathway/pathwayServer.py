import pathway as pw
from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm import llms, parsers
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import json
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# local = pw.io.fs.read(
#     "./data/",  # Pathway listens to this data folder
#     format="binary",  # Change from 'binary' to 'text'
#     # mode="streaming",
#     with_metadata=True,
# )

# gdrive = pw.io.gdrive.read(
#     object_id="14cPcPF19g3LPGojMTRhoNCFTAx8sTV0a",
#     service_user_credentials_file="../credentials.json"
# )

files = gdrive

unStructureParser = parsers.UnstructuredParser()
unstructured_documents = files.select(texts=unStructureParser(pw.this.data))
unstructured_documents = unstructured_documents.select(texts=strip_metadata(pw.this.texts))

prompt = unstructured_documents.select(prompt=build_prompt_structure(pw.this.texts))




# model_name = "BAAI/bge-small-en"
# model_kwargs = {"device": "cpu"}
# encode_kwargs = {"normalize_embeddings": True}


# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {'device': 'cpu'}
# encode_kwargs = {'normalize_embeddings': True}
# embeddings = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs
# )

# splitter = CharacterTextSplitter()

# parser = parsers.PypdfParser()

# host = "127.0.0.1"
# port = 8666

# server = VectorStoreServer.from_langchain_components(
#     *[local, gdrive], embedder=embeddings, splitter=splitter, parser=parser
# )

# server.run_server(
#     host=host,
#     port=port,
#     with_cache=True,
#     cache_backend=pw.persistence.Backend.filesystem("./Cache"),
#     # threaded=True
# )

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
