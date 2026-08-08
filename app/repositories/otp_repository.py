from sqlalchemy.orm import Session

from app.models.otp import PasswordOTP
from app.repositories.base_repository import BaseRepository


class OTPRepository(BaseRepository[PasswordOTP]):

    def __init__(self):
        super().__init__(PasswordOTP)

    def get_latest_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(PasswordOTP)
            .filter(
                PasswordOTP.user_id == user_id
            )
            .order_by(
                PasswordOTP.created_at.desc()
            )
            .first()
        )

    def get_valid_otp(
        self,
        db: Session,
        user_id: int,
        otp: str,
    ):
        return (
            db.query(PasswordOTP)
            .filter(
                PasswordOTP.user_id == user_id,
                PasswordOTP.otp == otp,
                PasswordOTP.is_verified == False,
            )
            .order_by(
                PasswordOTP.created_at.desc()
            )
            .first()
        )

    def get_verified_otp(
            self,
            db: Session,
            user_id: int,
    ):
        return (
            db.query(PasswordOTP)
            .filter(
                PasswordOTP.user_id == user_id,
                PasswordOTP.is_verified == True,
            )
            .order_by(
                PasswordOTP.created_at.desc()
            )
            .first()
        )