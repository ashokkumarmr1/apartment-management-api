# app/core/security.py

from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


# -------------------------
# Hash Password
# -------------------------
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# -------------------------
# Verify Password
# -------------------------
def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


# -------------------------
# Create JWT Token
# -------------------------
def create_access_token(data: dict) -> str:
    """
    Create JWT token.
    """

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# -------------------------
# Decode JWT Token
# -------------------------
def decode_access_token(token: str):
    """
    Verify and decode JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None