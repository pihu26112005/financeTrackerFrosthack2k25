from langchain_community.vectorstores import PathwayVectorClient


host = "127.0.0.1"
port = 8666


client = PathwayVectorClient(host=host, port=port)


query = "I wanna know expenditure in novemeber."
docs = client.similarity_search(query)
# print(docs)
# for i, doc in enumerate(docs, start=1):
#     print(f"Document {i}:")
#     print(doc)
#     print("-" * 50) 

# d2 = client.get_input_files()
# print(d2)