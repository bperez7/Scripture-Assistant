from pydantic import BaseModel, ConfigDict
from typing import List


class ScriptureVerseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    volume: str
    book: str
    chapter: int
    verse: int
    reference: str
    text: str


class BookResponse(BaseModel):
    name: str
    volume: str


class AskRequest(BaseModel):
    question: str


class Citation(BaseModel):
    reference: str
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]