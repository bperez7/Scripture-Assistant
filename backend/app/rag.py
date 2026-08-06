import os
from openai import OpenAI
from sqlalchemy.orm import Session

from app.models import ScriptureVerse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve_relevant_verses(question: str, db: Session):
    # MVP: simple keyword-ish search.
    # Later replace this with embeddings/vector search.
    keywords = question.split()

    query = db.query(ScriptureVerse)

    for word in keywords[:5]:
        query = query.filter(ScriptureVerse.text.ilike(f"%{word}%"))

    results = query.limit(8).all()

    if not results:
        results = db.query(ScriptureVerse).limit(5).all()

    return results


def answer_question(question: str, db: Session):
    verses = retrieve_relevant_verses(question, db)

    context = "\n\n".join(
        f"{v.reference}: {v.text}" for v in verses
    )

    prompt = f"""
You are an LDS scripture study assistant.

Use only the scripture passages provided below.
Do not invent doctrine.
If the answer is not clear from the provided passages, say that.

Question:
{question}

Scripture passages:
{context}

Answer with:
1. A helpful explanation
2. Specific scripture references
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You help users study LDS scripture with citations."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "citations": [
            {
                "reference": v.reference,
                "text": v.text,
            }
            for v in verses
        ],
    }