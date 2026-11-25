import re
from typing import Optional


SCRIPTURE_SITE = "https://www.churchofjesuschrist.org/study/scriptures"

# Gospel Library uses shortened paths for these books. Other paths use the
# lowercase book title, with hyphens in place of spaces.
BOOK_SLUGS = {
    "genesis": "gen",
    "exodus": "ex",
    "leviticus": "lev",
    "numbers": "num",
    "deuteronomy": "deut",
    "joshua": "josh",
    "judges": "judg",
    "1 samuel": "1-sam",
    "2 samuel": "2-sam",
    "1 kings": "1-kgs",
    "2 kings": "2-kgs",
    "1 chronicles": "1-chr",
    "2 chronicles": "2-chr",
    "nehemiah": "neh",
    "esther": "esth",
    "psalms": "ps",
    "proverbs": "prov",
    "ecclesiastes": "eccl",
    "song of solomon": "song",
    "isaiah": "isa",
    "jeremiah": "jer",
    "lamentations": "lam",
    "ezekiel": "ezek",
    "daniel": "dan",
    "obadiah": "obad",
    "habakkuk": "hab",
    "zephaniah": "zeph",
    "haggai": "hag",
    "zechariah": "zech",
    "malachi": "mal",
    "matthew": "matt",
    "romans": "rom",
    "1 corinthians": "1-cor",
    "2 corinthians": "2-cor",
    "galatians": "gal",
    "ephesians": "eph",
    "philippians": "philip",
    "colossians": "col",
    "1 thessalonians": "1-thes",
    "2 thessalonians": "2-thes",
    "1 timothy": "1-tim",
    "2 timothy": "2-tim",
    "philemon": "philem",
    "hebrews": "heb",
    "1 peter": "1-pet",
    "2 peter": "2-pet",
    "revelation": "rev",
    "1 nephi": "1-ne",
    "2 nephi": "2-ne",
    "3 nephi": "3-ne",
    "4 nephi": "4-ne",
    "words of mormon": "w-of-m",
    "helaman": "hel",
    "mormon": "morm",
    "moroni": "moro",
    "doctrine and covenants": "dc",
    "abraham": "abr",
    "articles of faith": "a-of-f",
    "joseph smith--history": "js-h",
    "joseph smith--matthew": "js-m",
}

VOLUME_SLUGS = {
    "old testament": "ot",
    "new testament": "nt",
    "book of mormon": "bofm",
    "doctrine and covenants": "dc-testament",
    "pearl of great price": "pgp",
}


def scripture_url(volume: str, book: str, chapter: int, verse: int) -> Optional[str]:
    collection = VOLUME_SLUGS.get((volume or "").strip().casefold())
    title = (book or "").strip().casefold()
    if not (collection and title and chapter and verse):
        return None
    slug = BOOK_SLUGS.get(title, title.replace(" ", "-"))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        return None
    return f"{SCRIPTURE_SITE}/{collection}/{slug}/{chapter}?lang=eng&id=p{verse}#p{verse}"
