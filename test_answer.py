from src.answer import generate_answer
from src.chunk_pdf import create_chunks
from src.retrieve import retrieve_documents


def test_create_chunks_preserves_source_and_page():
    pages = [
        {
            "page": 1,
            "source": "sample.pdf",
            "text": "An aortic aneurysm may have no symptoms. " * 20,
        }
    ]

    chunks = create_chunks(pages)

    assert len(chunks) > 0
    assert all(chunk["source"] == "sample.pdf" for chunk in chunks)
    assert all(chunk["page"] == 1 for chunk in chunks)
    assert all(chunk["text"].strip() for chunk in chunks)


def test_retrieve_documents_returns_relevant_chunks():
    documents = retrieve_documents(
        "What are the symptoms of an aortic aneurysm?"
    )

    assert isinstance(documents, list)
    assert len(documents) > 0

    for document in documents:
        assert document.get("text", "").strip()
        assert document.get("source")
        assert document.get("page") is not None

def test_generate_answer_returns_nonempty_response():
    question = "What are the symptoms of an aortic aneurysm?"
    documents = retrieve_documents(question)

    answer = generate_answer(question, documents)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0