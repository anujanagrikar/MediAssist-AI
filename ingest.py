from pubmed import PubMedRetriever
from chroma_manager import ChromaManager

manager = ChromaManager()

pmids = PubMedRetriever.search_pubmed_articles(
    "intermittent fasting",
    max_results=200
)

articles = PubMedRetriever.fetch_pubmed_abstracts(pmids)

for article in articles:
    manager.add_article(article)

print(f"Stored {len(articles)} articles")
