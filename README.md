
# Medical RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers medical questions using information retrieved from medical PDF documents.

## Features

- PDF text extraction and chunking
- Semantic embeddings using Sentence Transformers
- Vector search using Pinecone
- LLM-powered answers using Groq
- Source filenames and page references
- Flask-based web interface
- Automated tests using pytest
- Basic out-of-scope question handling

## Tech Stack

- Python 3.12
- Flask
- LangChain
- Hugging Face Sentence Transformers
- Pinecone
- Groq
- pytest
- HTML, CSS and JavaScript

## Project Structure

```text
Medical-RAG-Chatbot/
├── data/                 # Medical PDF documents
├── src/                  # RAG pipeline modules
├── static/               # CSS and JavaScript
├── templates/            # Flask HTML templates
├── app.py                # Web application
├── store_index.py        # Document indexing
├── test_answer.py        # Automated tests
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Install Python 3.12.
2. Clone this repository.
3. Create and activate a virtual environment.
4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and add your own API credentials.

   Required configuration:
   - `PINECONE_API_KEY`
   - `PINECONE_INDEX_NAME`
   - `GROQ_API_KEY`

6. Ensure the Pinecone index uses the embedding model's dimension of 384 and cosine similarity.

7. Index the documents:

   ```powershell
   python store_index.py
   ```

   **Warning:** The indexing script clears existing vectors in the configured index before uploading documents. Use a dedicated project index and understand this behavior before running it.

8. Start the web application:

   ```powershell
   python app.py
   ```

9. Open http://127.0.0.1:5000 in your browser.

## Run Tests

```powershell
python -m pytest -v
```

## Medical Safety

This project is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. For potentially life-threatening symptoms, seek emergency medical care.

## Future Improvements

- Improve retrieval evaluation and answer-grounding tests
- Add document upload support
- Add Docker support
- Set up CI using GitHub Actions
- Explore deployment on AWS
