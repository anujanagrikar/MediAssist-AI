import chromadb


class ChromaManager:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="pubmed_articles"
        )

    def add_article(self, article):

        document_text = article["title"]

        if "SUMMARY" in article["abstract"]:
            document_text += " " + article["abstract"]["SUMMARY"]

        self.collection.add(
            ids=[article["pmid"]],
            documents=[document_text],
            metadatas=[{
                "title": article["title"],
                "journal": article["journal"],
                "year": article["publication_date"]
            }]
        )

    def search(self, query, n_results=3):

        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )