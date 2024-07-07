from os import getenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends
from jose import JWTError, jwt
from fastapi import HTTPException, status
from starlette.status import HTTP_404_NOT_FOUND

from db import db

SECRET_KEY = getenv("AUTH_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

LoginFormData = Annotated[OAuth2PasswordRequestForm, Depends()]
BearerToken = Annotated[str, Depends(oauth2_scheme)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


UserNotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

InvalidCredsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

InvalidTokenError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


def login(form_data: LoginFormData) -> Token:
    user = db.Database().get_user(form_data.username)
    if not user:
        raise UserNotFoundError
    if not _verify_password(form_data.password, user.hashed_password):
        raise InvalidCredsError
    access_token = _create_access_token(
        data={"sub": user.name},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")

def authenticate(token: BearerToken) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenError
        token_data = TokenData(username=username)
    except JWTError:
        raise InvalidTokenError
    return token_data

def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password) -> str:
    return pwd_context.hash(password)