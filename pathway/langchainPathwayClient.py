from langchain_community.vectorstores import PathwayVectorClient


host = "127.0.0.1"
port = 8666


client = PathwayVectorClient(host=host, port=port)


query = "I want to know my transactions which have thier dates in november last year?"
docs = client.similarity_search(query, k=1)
print(client.get_vectorstore_statistics())
print(docs)
