# app/core/security.py

from jose import jwt

from datetime import datetime, timedelta, UTC

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        try:
            return password_hash.hash(password)
        except Exception as ex:
            raise RuntimeError("Failed to hash password.") from ex

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        try:
            return password_hash.verify(
                plain_password,
                hashed_password,
            )
        except Exception as ex:
            raise RuntimeError("Failed to verify password.") from ex

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        try:
            payload = data.copy()

            expire = (
                datetime.now(UTC)
                + (
                    expires_delta
                    or timedelta(
                        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                    )
                )
            )

            payload["exp"] = expire

            return jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
            )

        except Exception as ex:
            raise RuntimeError("Failed to create access token.") from ex

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

        except ExpiredSignatureError as ex:
            raise ValueError("Access token has expired.") from ex

        except InvalidTokenError as ex:
            raise ValueError("Invalid access token.") from ex

        except Exception as ex:
            raise RuntimeError("Failed to decode access token.") from ex