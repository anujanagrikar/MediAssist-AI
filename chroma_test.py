import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="pubmed_articles"
)

collection.add(
    ids=["test1"],
    documents=["Intermittent fasting may improve metabolic health."],
    metadatas=[{"source": "test"}]
)

print("Document added successfully!")