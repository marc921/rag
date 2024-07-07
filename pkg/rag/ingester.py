# The Ingester downloads the document from the URL, splits it into verses, and yields them for further processing.

from dataclasses import dataclass
from typing import Iterator
import requests
import re # Regular expressions

# DOCUMENT_URL="https://www.gutenberg.org/cache/epub/10/pg10.txt"	# King James Bible

@dataclass
class Verse:
    book: str
    chapter: int
    verse: int
    content: str

class Ingester:
    def ingest(self, doc_url: str, stop: int = -1) -> Iterator[Verse]:
        """Downloads (streams) the document from the URL, splits it into verses and sends them into the Embedder."""
        s = requests.Session()

        current_chunk = ""
        verse_pattern = r'\d+:\d+\s+' # Matches the chapter and verse number, indicating the start of a new verse
        newline_count = 0
        started = False
        ended = False
        book = ""
        chapter = -1
        verse = -1
        with s.get(doc_url, headers=None, stream=True) as resp:
            for line in resp.iter_lines():
                if not line:
                    newline_count += 1
                    if newline_count == 4 and current_chunk:
                        # 4 consecutive newlines indicate the end of a book
                        yield Verse(
                            book=book if book else None,
                            chapter=chapter if chapter != -1 else None,
                            verse=verse if verse != -1 else None,
                            content=current_chunk,
                        )
                        current_chunk = ""
                        newline_count = 0
                        book = ""
                    continue
                newline_count = 0
                line: str = line.decode("utf-8") # Convert bytes to string
                if not started:
                    if line == "*** START OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***":
                        started = True
                    continue
                if not ended:
                    if line == "*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***":
                        ended = True
                        break
                while match := re.search(verse_pattern, line):
                    current_chunk += line[:match.start()]
                    if current_chunk:
                        yield Verse(
                            book=book if book else None,
                            chapter=chapter if chapter != -1 else None,
                            verse=verse if verse != -1 else None,
                            content=current_chunk,
                        )
                        current_chunk = ""
                    current_chunk = match.group()
                    chapter, verse = map(int, current_chunk.split(":"))
                    line = line[match.end():]
                current_chunk += line + " "
                if not book:
                    book = current_chunk.strip()
                stop -= 1
                if stop == 0:
                    return