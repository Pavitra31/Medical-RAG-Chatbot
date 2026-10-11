from pathlib import Path
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip(),
                "source": pdf_path.name,
            })

    return pages



if __name__ == "__main__":
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
    else:
        pages = extract_pdf_text(PDF_PATH)
        print(f"Pages with text: {len(pages)}")

        for page in pages[:2]:
            print(f"\n--- Page {page['page']} ---")
            print(page["text"][:1000])
