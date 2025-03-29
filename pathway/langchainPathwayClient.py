from langchain_community.vectorstores import PathwayVectorClient


host = "127.0.0.1"
port = 8666


client = PathwayVectorClient(host=host, port=port)


query = "What is LuvSharma"
docs = client.similarity_search(query)
print(docs)
