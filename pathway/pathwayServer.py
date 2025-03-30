import pathway as pw
from pathway.xpacks.llm.vector_store import VectorStoreServer
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathway.xpacks.llm import llms, parsers, splitters, embedders
from pathway.xpacks.llm.prompts import Build


# Read data correctly
local = pw.io.fs.read(
    "./data/",  # Pathway listens to this data folder
    format="binary",  # Change from 'binary' to 'text'
    # mode="streaming",
    with_metadata=True,
)

gdrive = pw.io.gdrive.read(
    object_id="14cPcPF19g3LPGojMTRhoNCFTAx8sTV0a",
    service_user_credentials_file="credentials.json"
)

files = gdrive

unStructureParser = parsers.UnstructuredParser()
unstructured_documents = files.select(texts=unStructureParser(pw.this.data))
unstructured_documents = unstructured_documents.select(texts=strip_metadata(pw.this.texts))

prompt = unstructured_documents.select(prompt=build_prompt_structure(pw.this.texts))




# Model parameters

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


# Define your text splitter with appropriate settings
# splitter = RecursiveCharacterTextSplitter(
#     separators=["\n\n", "\n", " ", ""],
# )

splitter = splitters.TokenCountSplitter()
parser = parsers.PypdfParser()

# Server parameters
host = "127.0.0.1"
port = 8666

# Start vector store server
server = VectorStoreServer.from_langchain_components(
    *[local, gdrive], embedder=embeddings, parser=parser

)

server.docs

server.run_server(
    host=host,
    port=port,
    with_cache=True,
    cache_backend=pw.persistence.Backend.filesystem("./Cache"),
    # threaded=True
)


