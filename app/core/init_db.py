from sqlalchemy import create_engine, text

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base

# Import all models (VERY IMPORTANT)
from app.models.role import Role
from app.models.apartment import Apartment
from app.models.user import User

server_engine = create_engine(
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
)


def create_database():
    with server_engine.connect() as conn:
        conn.execute(
            text(f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}`")
        )
        conn.commit()

    print("Database Ready")


def create_tables():
    print("Creating tables...")
    print("Registered tables:", list(Base.metadata.tables.keys()))

    Base.metadata.create_all(bind=engine)

    print("Tables Ready")