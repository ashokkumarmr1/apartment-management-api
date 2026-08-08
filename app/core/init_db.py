from sqlalchemy import create_engine, text

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models.base import Base

from app.services.role_service import RoleService

from app.models.role import Role
from app.models.apartment import Apartment
from app.models.user import User

from app.models import User, Role, Apartment, PasswordOTP


server_engine = create_engine(
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
)


class InitDB:

    @staticmethod
    def create_database():
        with server_engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}`"
                )
            )
            conn.commit()

        print("Database Ready")

    @staticmethod
    def create_tables():
        print("Creating tables...")
        print("Registered tables:", list(Base.metadata.tables.keys()))

        Base.metadata.create_all(bind=engine)

        print("Tables Ready")

    @staticmethod
    def seed_data():
        db = SessionLocal()

        try:
            RoleService.seed_roles(db)
        finally:
            db.close()

        print("Default Roles Ready")

    @classmethod
    def initialize(cls):
        cls.create_database()
        cls.create_tables()
        cls.seed_data()