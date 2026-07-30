from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.models.base import BaseModel


class Apartment(BaseModel):
    __tablename__ = "apartments"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship back to User
    users: Mapped[list["User"]] = relationship("User", back_populates="apartment")

