# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.core.dependencies import get_db
from app.schemas.user import UserRegister, UserLogin
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

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "User registered successfully.",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "mobile": user.mobile
                }
            }
        )


    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
                "data": None
            }
        )


    except Exception as e:
        print(e)
        raise

@router.post("/login")
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        result = service.login(db, request)

        user = result["user"]
        access_token = result["access_token"]

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "access_token": access_token,
                "token_type": "Bearer",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "mobile": user.mobile,
                    "role_id": user.role_id,
                    "apartment_id": user.apartment_id
                }
            }
        }

    except ValueError as e:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": str(e),
                "data": None
            }
        )