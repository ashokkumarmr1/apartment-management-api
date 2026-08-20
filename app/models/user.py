from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.otp import PasswordOTP
from app.models.role import Role
from app.models.apartment import Apartment
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.visitor import Visitor


class User(BaseModel):
    __tablename__ = "users"


    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    mobile: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.id"),
        nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users"
    )

    apartment: Mapped["Apartment"] = relationship(
        "Apartment",
        back_populates="users"
    )

    password_otps: Mapped[list["PasswordOTP"]] = relationship(
        "PasswordOTP",
        back_populates="user",
    )

    visitors: Mapped[list["Visitor"]] = relationship(
        "Visitor",
        back_populates="creator",
    )