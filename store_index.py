
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.read_pdf import extract_pdf_text, DATA_DIR
from src.chunk_pdf import create_chunks

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-rag-index")


def main():
    if not API_KEY:
        raise ValueError("PINECONE_API_KEY is missing from .env")

    print("Reading PDFs...")
    pages = []

    for pdf_path in DATA_DIR.glob("*.pdf"):
        pages.extend(extract_pdf_text(pdf_path))

    chunks = create_chunks(pages)

    if not chunks:
        raise ValueError("No chunks found in the data folder.")

    print(f"Created {len(chunks)} chunks from PDF files.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    pc = Pinecone(api_key=API_KEY)
    index = pc.Index(INDEX_NAME)

    print("Clearing old vectors...")
    index.delete(delete_all=True)

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
    )

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "page": chunk["page"],
            "chunk": chunk["chunk"],
            "source": chunk["source"],
        }
        for chunk in chunks
    ]

    print("Uploading updated chunks...")
    vector_store.add_texts(texts=texts, metadatas=metadatas)

    print(f"Success! Uploaded {len(texts)} chunks to Pinecone.")


if __name__ == "__main__":
    main()
