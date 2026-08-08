# app/api/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.responses import ApiResponse
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserLogin
)
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest

from app.core.dependencies import (
    get_db,
    get_current_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

service = AuthService()


@router.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    user = service.register(db, request)

    return ApiResponse.success(
        message="User registered successfully.",
        status_code=201,
        data={
            "id": user.id,
            "full_name": user.full_name,
            "mobile": user.mobile,
        },
    )


@router.post("/login")
def login(
    request: UserLogin,
    db: Session = Depends(get_db),
):
    result = service.login(db, request)

    user = result["user"]

    return ApiResponse.success(
        message="Login successful.",
        data={
            "access_token": result["access_token"],
            "token_type": "Bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "mobile": user.mobile,
                "role_id": user.role_id,
                "apartment_id": user.apartment_id,
            },
        },
    )


@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        service.change_password(
            db,
            current_user,
            request,
        )

        return ApiResponse.success(
            message="Password changed successfully.",
        )

    except ValueError as e:
        return ApiResponse.error(
            message=str(e),
            status_code=400,
        )

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "success": True,
        "message": "User details fetched successfully.",
        "data": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "mobile": current_user.mobile,
            "role_id": current_user.role_id,
            "apartment_id": current_user.apartment_id,
        },
    }