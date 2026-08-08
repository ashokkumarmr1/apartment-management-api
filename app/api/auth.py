# app/api/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.responses import ApiResponse
from app.models import PasswordOTP
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserLogin
)
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest

from app.schemas.auth import ForgotPasswordRequest
from app.services.otp_service import OTPService

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.schemas.auth import (
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

service = AuthService()
otp_service = OTPService()


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

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    try:

        otp = otp_service.request_password_reset(
            db,
            request.mobile,
        )

        return {
            "success": True,
            "message": "OTP generated successfully.",
            "data": {
                "otp": otp.otp,
                "expires_at": otp.expires_at,
            },
        }

    except ValueError as e:

        return {
            "success": False,
            "message": str(e),
            "data": None,
        }

def verify_password_reset_otp(
    self,
    db: Session,
    mobile: str,
    otp: str,
) -> PasswordOTP:

    user = self.user_repository.get_by_mobile(
        db,
        mobile,
    )

    if user is None:
        raise ValueError("User not found.")

    return self.verify_password_otp(
        db,
        user.id,
        otp,
    )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        otp_service.reset_password(
            db,
            request.mobile,
            request.new_password,
        )

        return {
            "success": True,
            "message": "Password reset successfully.",
            "data": None,
        }

    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "data": None,
        }
