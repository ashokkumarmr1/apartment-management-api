from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class PasswordOTP(BaseModel):
    __tablename__ = "password_otps"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    otp: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="password_otps",
    )