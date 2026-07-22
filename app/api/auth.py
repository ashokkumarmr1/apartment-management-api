# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.user import UserRegister
from app.services.auth_service import AuthService

router = APIRouter()

service = AuthService()


@router.post("/register", status_code=201)
def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        user = service.register(db, request)

        return {
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    except Exception as e:

        print(e)

        raise