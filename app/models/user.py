from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    mobile = Column(String(15), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    gender = Column(
        Enum("Male", "Female", "Other", name="gender_enum"),
        nullable=True
    )

    role_id = Column(
        BigInteger,
        nullable=False
    )

    apartment_id = Column(
        BigInteger,
        nullable=False
    )

    status = Column(
        Enum(
            "ACTIVE",
            "INACTIVE",
            "BLOCKED",
            "PENDING",
            name="user_status_enum"
        ),
        default="ACTIVE",
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    deleted_at = Column(
        TIMESTAMP,
        nullable=True
    )

    # Relationships
   # role = relationship("Role", back_populates="users")
   # apartment = relationship("Apartment", back_populates="users")