from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.apartment import Apartment
    from app.models.user import User


class Visitor(BaseModel):
    __tablename__ = "visitors"

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.id"),
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    visitor_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    vehicle_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    visitor_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    purpose: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    expected_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    check_in_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    check_out_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="EXPECTED",
    )

    apartment: Mapped["Apartment"] = relationship(
        "Apartment",
        back_populates="visitors",
    )

    creator: Mapped["User"] = relationship(
        "User",
        back_populates="visitors",
    )