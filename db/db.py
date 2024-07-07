
from os import getenv
from sqlalchemy import create_engine

from db.sqlcgen import models, users, verses

class Database:
    def __init__(self):
        database_url = getenv('DATABASE_URL')
        self.engine = create_engine(database_url)

    def get_user(self, username: str) -> models.User | None:
        with self.engine.connect() as conn:
            user_querier = users.Querier(conn)
            return user_querier.get_user(name=username)
    
    def insert_user(self, username: str, hashed_password: str) -> models.User | None:
        with self.engine.connect() as conn:
            user_querier = users.Querier(conn)
            user = user_querier.insert_user(name=username, hashed_password=hashed_password)
            conn.commit()
            return user

    def insert_verse(self, book: str, chapter: int, verse: int, content: str, embedding: list[float]) -> models.Verse | None:
        with self.engine.connect() as conn:
            verse_querier = verses.Querier(conn)
            verse = verse_querier.insert_verse(
                verses.InsertVerseParams(
                    book=book,
                    chapter=chapter,
                    verse=verse,
                    content=content, 
                    embedding=embedding,
                ),
            )
            conn.commit()
            return verse

    def get_similar_verses(self, embedding: list[float], limit: int) -> list[models.Verse]:
        with self.engine.connect() as conn:
            verse_querier = verses.Querier(conn)
            embedding_str = '[' + ','.join(map(str, embedding)) + ']'
            return list(verse_querier.get_similar_verses(embedding=embedding_str, limit=limit))