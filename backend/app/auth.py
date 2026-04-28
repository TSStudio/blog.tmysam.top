from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status

from .config import settings


def create_token() -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": "admin",
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_password(password: str) -> bool:
    return password == settings.admin_password


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
