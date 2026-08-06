from sqlalchemy import Column, Integer, String, Text
from app.db import Base


class ScriptureVerse(Base):
    __tablename__ = "scripture_verses"

    id = Column(Integer, primary_key=True, index=True)

    volume = Column(String, index=True)   # Book of Mormon, Bible, D&C, Pearl of Great Price
    book = Column(String, index=True)     # Alma, Nephi, Matthew, etc.
    chapter = Column(Integer, index=True)
    verse = Column(Integer, index=True)

    reference = Column(String, index=True)  # Alma 32:21
    text = Column(Text, nullable=False)