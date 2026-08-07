# app/core/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import Security
from app.repositories.user_repository import UserRepository


# ----------------------------------
# JWT Security
# ----------------------------------

security = HTTPBearer()

user_repository = UserRepository()


# ----------------------------------
# Database Dependency
# ----------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ----------------------------------
# Get Current User
# ----------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:

        # Decode JWT
        payload = Security.decode_access_token(token)

        # Get user ID from JWT
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Find user
        user = user_repository.get_by_id(
            db,
            int(user_id),
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        )