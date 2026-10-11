try:
    from src.read_pdf import extract_pdf_text, DATA_DIR
except ModuleNotFoundError:
    from read_pdf import extract_pdf_text, DATA_DIR
    
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk_number, text in enumerate(page_chunks, start=1):
            chunks.append({
                "text": text,
                "page": page["page"],
                "chunk": chunk_number,
                "source": page["source"],
            })

    return chunks

if __name__ == "__main__":
    all_pages = []

    for pdf_path in DATA_DIR.glob("*.pdf"):
        all_pages.extend(extract_pdf_text(pdf_path))

    chunks = create_chunks(all_pages)
    print(f"PDFs found: {len(list(DATA_DIR.glob('*.pdf')))}")
    print(f"Total chunks created: {len(chunks)}")

    for chunk in chunks[:3]:
        print(f"\n--- {chunk['source']} | Page {chunk['page']} ---")
        print(chunk["text"])
