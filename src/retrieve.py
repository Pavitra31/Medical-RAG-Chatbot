
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-rag-index")


def retrieve_documents(question, k=3):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings,
    )

    results = vector_store.similarity_search_with_score(question, k=k)

    return [
    {
        "text": doc.page_content,
        "page": doc.metadata.get("page", "Unknown"),
        "source": doc.metadata.get("source", "Unknown"),
        "score": score,
    }
    for doc, score in results
]


if __name__ == "__main__":
    question = input("Ask a medical question: ").strip()

    if question:
        print("\nSearching your medical PDFs...")
        try:
            results = retrieve_documents(question)

            for i, result in enumerate(results, start=1):
                print(
                    f"\n--- Result {i} | "
                    f"{result['source']} | Page {result['page']} ---"
                )
                print(f"Similarity score: {result['score']:.4f}")
                print(result["text"])
        except Exception as error:
            print(f"Retrieval failed: {error}")
    else:
        print("Please enter a question.")
