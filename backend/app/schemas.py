from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


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


class ChapterContext(BaseModel):
    volume: str
    book: str
    chapter: int


class AskRequest(BaseModel):
    question: str
    chapter_context: Optional[ChapterContext] = None


class Citation(BaseModel):
    reference: str
    text: str


class WebSource(BaseModel):
    title: str
    url: str


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
    web_sources: List[WebSource] = Field(default_factory=list)
