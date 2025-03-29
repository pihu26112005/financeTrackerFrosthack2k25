import pathway as pw
import pathway.persistence
from pathway.xpacks.llm.vector_store import VectorStoreServer
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Read data correctly
data = pw.io.fs.read(
    "./data",  # Pathway listens to this data folder
    format="binary",  # Change from 'binary' to 'text'
    mode="streaming",
    with_metadata=True,
)

# Model parameters
model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)
splitter = CharacterTextSplitter()

# Server parameters
host = "127.0.0.1"
port = 8666

# Start vector store server
server = VectorStoreServer.from_langchain_components(
    data, embedder=embeddings, splitter=splitter
)

server.run_server(
    host=host,
    port=port,
    with_cache=True,
    cache_backend=pw.persistence.Backend.filesystem("./Cache"),
    threaded=True
)
