from chroma_manager import ChromaManager
from generator import build_context, generate_answer


def main():

    manager = ChromaManager()

    question = input("Ask a healthcare question: ")

    # Retrieve relevant articles
    results = manager.search(
        query=question,
        n_results=5
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        print("\nNo relevant articles found.")
        return

    # Build context for LLM
    context = build_context(results)

    # Generate answer using Groq
    answer = generate_answer(
        question,
        context
    )

    # Display answer
    print("\n" + "=" * 70)
    print("MEDIASSIST AI ANSWER")
    print("=" * 70)
    print(answer)

    # Display sources
    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for i, meta in enumerate(metadatas, start=1):

        print(f"\nSource {i}")
        print(f"Title   : {meta.get('title', 'Not Available')}")
        print(f"Journal : {meta.get('journal', 'Not Available')}")
        print(f"Year    : {meta.get('year', 'Not Available')}")

    # Optional: Show retrieved evidence
    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for i, doc in enumerate(documents, start=1):
        print(f"\nArticle {i}")
        print("-" * 70)
        print(doc[:500])


if __name__ == "__main__":
    main()