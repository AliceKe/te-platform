from datetime import datetime, timedelta
from typing import Any

import app.ents.user.crud as user_crud
import app.ents.user.models as user_models
from app.core.settings import settings
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str = ""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """
    Creates an access token with `subject` that expires after `expires_delta`.
    """

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if `plain_password` is `hashed_password`.
    """
    return pwd_context.verify(plain_password, hashed_password)


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except JWTError:
        return None


def authenticate(db: Session, *, email: str, password: str) -> user_models.User:
    user = user_crud.read_user_by_email(db, email=email)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None
    return user


def is_superuser(user) -> bool:
    ...
