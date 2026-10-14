from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import distinct
from sqlalchemy.orm import Session
from typing import Optional

from app.db import Base, engine, get_db
from app.models import ScriptureVerse
from app.schemas import (
    AskRequest,
    AskResponse,
    ScriptureVerseResponse,
)
from app.rag import answer_question

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LDS AI Gospel Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "LDS AI Gospel Library API"}


@app.get("/scriptures/volumes")
def get_volumes(db: Session = Depends(get_db)):
    rows = (
        db.query(distinct(ScriptureVerse.volume))
        .order_by(ScriptureVerse.volume)
        .all()
    )

    return [row[0] for row in rows]


@app.get("/scriptures/books")
def get_books(
    volume: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(
        ScriptureVerse.book,
        ScriptureVerse.volume,
    ).distinct()

    if volume:
        query = query.filter(ScriptureVerse.volume == volume)

    rows = query.order_by(
        ScriptureVerse.volume,
        ScriptureVerse.id,
    ).all()

    return [
        {
            "name": row.book,
            "volume": row.volume,
        }
        for row in rows
    ]


@app.get("/scriptures/books/{book}/chapters")
def get_chapters(
    book: str,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(distinct(ScriptureVerse.chapter))
        .filter(ScriptureVerse.book == book)
        .order_by(ScriptureVerse.chapter)
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="Book not found")

    return [row[0] for row in rows]


@app.get(
    "/scriptures/books/{book}/chapters/{chapter}",
    response_model=list[ScriptureVerseResponse],
)
def get_chapter(
    book: str,
    chapter: int,
    db: Session = Depends(get_db),
):
    verses = (
        db.query(ScriptureVerse)
        .filter(
            ScriptureVerse.book == book,
            ScriptureVerse.chapter == chapter,
        )
        .order_by(ScriptureVerse.verse)
        .all()
    )

    if not verses:
        raise HTTPException(
            status_code=404,
            detail="Chapter not found",
        )

    return verses


@app.get(
    "/scriptures/search",
    response_model=list[ScriptureVerseResponse],
)
def search_scriptures(
    q: str,
    db: Session = Depends(get_db),
):
    return (
        db.query(ScriptureVerse)
        .filter(ScriptureVerse.text.ilike(f"%{q}%"))
        .limit(25)
        .all()
    )


@app.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    return answer_question(request.question, db)
