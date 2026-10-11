
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def generate_answer(question, retrieved_documents):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not retrieved_documents:
        return "I couldn't find relevant information in the available medical sources."

    context_parts = []
    for doc in retrieved_documents:
        context_parts.append(
            f"Source: {doc['source']}, page {doc['page']}\n{doc['text']}"
        )

    context = "\n\n".join(context_parts)

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key,
    )

    prompt = f"""
You are a medical information assistant for educational purposes.
Answer the user's question using only the supplied context.
Do not diagnose, prescribe medication, or invent facts.
If the context does not answer the question, say so clearly.
Cite the source filename and page number when possible.
For potentially life-threatening symptoms, advise urgent medical care.

Context:
{context}

Question: {question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content
