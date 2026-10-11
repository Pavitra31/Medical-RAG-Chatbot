
from flask import Flask, render_template, request, jsonify
from pathlib import Path
from dotenv import load_dotenv
import markdown
import bleach

from src.retrieve import retrieve_documents
from src.answer import generate_answer

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

app = Flask(__name__)

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li",
    "h2", "h3", "h4", "blockquote", "code", "pre",
    "a", "hr",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}

ALLOWED_PROTOCOLS = ["https", "http", "mailto"]


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if len(question) > 1000:
        return jsonify({
            "error": "Please keep your question under 1000 characters."
        }), 400

    try:
        documents = retrieve_documents(question)
        answer = generate_answer(question, documents)

        # Convert Markdown to HTML, then sanitize before rendering.
        rendered_html = markdown.markdown(
            answer,
            extensions=["extra", "sane_lists"],
        )
        safe_html = bleach.clean(
            rendered_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
        )

        sources = sorted({
            f"{doc.get('source', 'Unknown source')}, "
            f"page {doc.get('page', 'Unknown')}"
            for doc in documents
        })

        return jsonify({
            "answer_html": safe_html,
            "sources": sources,
        })

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": (
                "The chatbot couldn't answer right now. "
                "Please try again shortly."
            )
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
