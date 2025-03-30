from langchain_community.vectorstores import PathwayVectorClient


host = "127.0.0.1"
port = 8666


client = PathwayVectorClient(host=host, port=port)


query = "transactions of janury 2023"
docs = client.similarity_search(query,k=30)
# print(docs)
for i, doc in enumerate(docs, start=1):
    print(f"Document {i}:")
    print(doc)
    print("-" * 50) 

# print(client.get_vectorstore_statistics())
# print(client.get_input_files())
