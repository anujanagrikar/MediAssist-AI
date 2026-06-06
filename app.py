import streamlit as st
import chromadb

from pubmed import PubMedRetriever
from chroma_manager import ChromaManager
from generator import build_context, generate_answer


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def clear_collection():

    try:
        client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        client.delete_collection(
            "pubmed_articles"
        )

        st.sidebar.success(
            "Knowledge Base Cleared Successfully!"
        )

    except Exception as e:

        st.sidebar.warning(
            f"Collection not found: {e}"
        )


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MediAssist AI")
st.caption(
    "Evidence-Based Healthcare Assistant powered by PubMed + ChromaDB + Groq"
)

# --------------------------------------------------
# Initialize Chroma
# --------------------------------------------------

manager = ChromaManager()

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "articles" not in st.session_state:
    st.session_state.articles = []

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("📚 PubMed Document Search")

search_term = st.sidebar.text_input(
    "Search Topic",
    value="intermittent fasting"
)

max_articles = st.sidebar.slider(
    "Number of Articles",
    min_value=10,
    max_value=300,
    value=100,
    step=10
)

# --------------------------------------------------
# Search PubMed
# --------------------------------------------------

if st.sidebar.button("🔍 Search PubMed"):

    with st.spinner("Searching PubMed..."):

        pmids = PubMedRetriever.search_pubmed_articles(
            search_term,
            max_results=max_articles
        )

        articles = PubMedRetriever.fetch_pubmed_abstracts(
            pmids
        )

        st.session_state.articles = articles

    st.sidebar.success(
        f"Retrieved {len(articles)} articles"
    )

# --------------------------------------------------
# Display Retrieved Articles
# --------------------------------------------------

if st.session_state.articles:

    st.sidebar.markdown("---")
    st.sidebar.subheader("Retrieved Articles")

    for article in st.session_state.articles[:10]:

        st.sidebar.write(
            f"• {article['title'][:60]}..."
        )

# --------------------------------------------------
# Ingest Documents
# --------------------------------------------------

if st.sidebar.button("📥 Ingest Documents"):

    if not st.session_state.articles:

        st.sidebar.warning(
            "Search PubMed first."
        )

    else:

        with st.spinner(
                "Ingesting documents into vector store..."):

            count = 0

            for article in st.session_state.articles:

                try:
                    manager.add_article(article)
                    count += 1

                except Exception:
                    pass

        st.sidebar.success(
            f"Ingested {count} articles into ChromaDB"
        )

# --------------------------------------------------
# Database Management
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader(
    "⚙️ Database Management"
)

st.sidebar.info(
    "Clearing the knowledge base permanently removes all stored articles."
)

if st.sidebar.button(
        "🗑️ Clear Knowledge Base"
):

    clear_collection()

# --------------------------------------------------
# Main Q&A Section
# --------------------------------------------------

st.markdown("---")

st.header("💬 Ask a Healthcare Question")

question = st.text_input(
    "Enter your question",
    placeholder="What are the health benefits of intermittent fasting?"
)

top_k = st.slider(
    "Number of Documents for Retrieval",
    min_value=3,
    max_value=10,
    value=5
)

# --------------------------------------------------
# Generate Answer
# --------------------------------------------------

if st.button("🚀 Get Answer"):

    if not question.strip():

        st.warning(
            "Please enter a healthcare question."
        )

    else:

        with st.spinner(
                "Searching knowledge base and generating answer..."):

            results = manager.search(
                query=question,
                n_results=top_k
            )

            documents = results.get(
                "documents",
                [[]]
            )[0]

            if not documents:

                st.error(
                    "No relevant documents found."
                )

            else:

                context = build_context(
                    results
                )

                answer = generate_answer(
                    question,
                    context
                )

                st.success(
                    "Answer generated successfully!"
                )

                # ------------------------------------------
                # Answer
                # ------------------------------------------

                st.subheader("🧠 Answer")

                st.write(answer)

                # ------------------------------------------
                # Sources
                # ------------------------------------------

                st.subheader("📄 Sources")

                metadatas = results.get(
                    "metadatas",
                    [[]]
                )[0]

                for i, meta in enumerate(
                        metadatas,
                        start=1):

                    with st.expander(
                            f"Source {i}"):

                        st.write(
                            f"**Title:** {meta.get('title', 'N/A')}"
                        )

                        st.write(
                            f"**Journal:** {meta.get('journal', 'N/A')}"
                        )

                        st.write(
                            f"**Year:** {meta.get('year', 'N/A')}"
                        )

                # ------------------------------------------
                # Retrieved Context
                # ------------------------------------------

                with st.expander(
                        "🔍 Retrieved Context"):

                    st.text(
                        context[:5000]
                    )