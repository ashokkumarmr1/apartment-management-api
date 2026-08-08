import secrets
from datetime import datetime, timedelta, UTC

from sqlalchemy.orm import Session

from app.core.security import Security
from app.models.otp import PasswordOTP
from app.repositories.otp_repository import OTPRepository
from app.repositories.user_repository import UserRepository


class OTPService:

    OTP_EXPIRY_MINUTES = 5

    def __init__(self):
        self.otp_repository = OTPRepository()
        self.user_repository = UserRepository()

    def generate_otp(self) -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    def create_password_otp(
        self,
        db: Session,
        user_id: int,
    ) -> PasswordOTP:

        otp = self.generate_otp()

        expires_at = (
            datetime.now(UTC)
            + timedelta(
                minutes=self.OTP_EXPIRY_MINUTES
            )
        )

        password_otp = PasswordOTP(
            user_id=user_id,
            otp=otp,
            expires_at=expires_at,
            is_verified=False,
        )

        return self.otp_repository.create(
            db,
            password_otp,
        )

    def verify_password_otp(
        self,
        db: Session,
        user_id: int,
        otp: str,
    ) -> PasswordOTP:

        password_otp = self.otp_repository.get_valid_otp(
            db,
            user_id,
            otp,
        )

        if password_otp is None:
            raise ValueError(
                "Invalid OTP."
            )

        now = datetime.now(UTC)

        if password_otp.expires_at < now:
            raise ValueError(
                "OTP has expired."
            )

        password_otp.is_verified = True

        return self.otp_repository.update(
            db,
            password_otp,
        )

    def request_password_reset(
            self,
            db: Session,
            mobile: str,
    ) -> PasswordOTP:

        user = self.user_repository.get_by_mobile(
            db,
            mobile,
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        return self.create_password_otp(
            db,
            user.id,
        )

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
            raise ValueError(
                "User not found."
            )

        return self.verify_password_otp(
            db,
            user.id,
            otp,
        )

    def reset_password(
            self,
            db: Session,
            mobile: str,
            new_password: str,
    ):
        user = self.user_repository.get_by_mobile(
            db,
            mobile,
        )

        if user is None:
            raise ValueError("User not found.")

        verified_otp = self.otp_repository.get_verified_otp(
            db,
            user.id,
        )

        if verified_otp is None:
            raise ValueError(
                "Please verify OTP before resetting password."
            )

        # Hash new password
        user.password_hash = Security.hash_password(
            new_password
        )

        # Consume OTP
        verified_otp.is_verified = False

        self.user_repository.update(
            db,
            user,
        )

        self.otp_repository.update(
            db,
            verified_otp,
        )

        return user