from dataclasses import dataclass
from typing import Annotated
from fastapi import Depends, FastAPI
from hash import hash_array

from pkg import auth
from pkg.rag import ingester, embedder
from db import db
from db.sqlcgen import models

app = FastAPI()

@app.post("/token")
async def login_for_access_token(
    form_data: auth.LoginFormData
) -> auth.Token:
    return auth.login(form_data)

@dataclass
class UserRequest:
    username: str
    password: str

@app.post("/users")
async def insert_user(
    body: UserRequest
):
    hashed_password = auth.pwd_context.hash(body.password)
    user = db.Database().insert_user(body.username, hashed_password)
    return user

def get_current_user(
    token_data: Annotated[auth.TokenData, Depends(auth.authenticate)],
) -> models.User:
    user = db.Database().get_user(token_data.username)
    if not user:
        raise auth.InvalidCredsError
    return user

@app.get("/users/me", response_model=models.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    return current_user

@dataclass
class IngestRequest:
    doc_url: str
    stop: int

@app.post("/rag/ingest")
async def ingest(
    body: IngestRequest
):
    ing = ingester.Ingester()
    emb = embedder.Embedder()
    verse_iterator = ing.ingest(doc_url=body.doc_url, stop=body.stop)
    for verse in verse_iterator:
        embedding = emb.embed(verse.content)
        print(verse, hash_array(embedding))
        verse = db.Database().insert_verse(
            book=verse.book,
            chapter=verse.chapter,
            verse=verse.verse,
            content=verse.content,
            embedding=embedding
        )
    return {"status": "success"}


@dataclass
class GetSimilarRequest:
    text: str
    limit: int = 5
    with_embeddings: bool = False

@app.post("/rag/similar")
async def get_similar(
    body: GetSimilarRequest
):
    emb = embedder.Embedder()
    embedding = emb.embed(body.text)
    similar_verses = db.Database().get_similar_verses(embedding=embedding, limit=body.limit)
    if not body.with_embeddings:
        for verse in similar_verses:
            verse.embedding = None # embeddings ruin the output
    return similar_verses
