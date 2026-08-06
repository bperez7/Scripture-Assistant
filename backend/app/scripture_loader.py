import json
import sys
from pathlib import Path
from typing import Any

from app.db import Base, SessionLocal, engine
from app.models import ScriptureVerse

Base.metadata.create_all(bind=engine)


def first_present(
    item: dict[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    for key in keys:
        if key in item and item[key] is not None:
            return item[key]

    return default


def extract_records(data: Any) -> list[dict[str, Any]]:
    """
    Supports:
      - a top-level JSON array
      - {"scriptures": [...]}
      - {"verses": [...]}
      - {"data": [...]}
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("scriptures", "verses", "data"):
            value = data.get(key)

            if isinstance(value, list):
                return value

    raise ValueError(
        "Could not locate a scripture record list in the JSON file."
    )


def normalize_record(item: dict[str, Any]) -> ScriptureVerse:
    volume = first_present(
        item,
        "volume_title",
        "volume",
        "volume_name",
    )

    book = first_present(
        item,
        "book_title",
        "book",
        "book_name",
    )

    chapter = first_present(
        item,
        "chapter_number",
        "chapter",
    )

    verse = first_present(
        item,
        "verse_number",
        "verse",
    )

    text = first_present(
        item,
        "scripture_text",
        "text",
        "verse_text",
    )

    reference = first_present(
        item,
        "verse_short_title",
        "reference",
        "verse_title",
    )

    if not reference and book and chapter and verse:
        reference = f"{book} {chapter}:{verse}"

    missing = [
        name
        for name, value in {
            "volume": volume,
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "text": text,
        }.items()
        if value is None
    ]

    if missing:
        raise ValueError(
            f"Record is missing required fields: {missing}. "
            f"Record: {item}"
        )

    return ScriptureVerse(
        volume=str(volume),
        book=str(book),
        chapter=int(chapter),
        verse=int(verse),
        reference=str(reference),
        text=str(text),
    )


def load_scriptures(path: str) -> None:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    records = extract_records(data)

    db = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for item in records:
            try:
                verse = normalize_record(item)
            except (TypeError, ValueError) as error:
                print(f"Skipping record: {error}")
                skipped += 1
                continue

            existing = (
                db.query(ScriptureVerse)
                .filter(
                    ScriptureVerse.volume == verse.volume,
                    ScriptureVerse.book == verse.book,
                    ScriptureVerse.chapter == verse.chapter,
                    ScriptureVerse.verse == verse.verse,
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            db.add(verse)
            inserted += 1

        db.commit()

        print(f"Inserted {inserted} verses.")
        print(f"Skipped {skipped} verses.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python -m app.scripture_loader "
            "/path/to/scriptures.json"
        )
        raise SystemExit(1)

    load_scriptures(sys.argv[1])