from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(BigInteger, primary_key=True, index=True)
    apartment_name = Column(String(100), nullable=False)

    users = relationship("User", back_populates="apartment")