# app/services/auth_service.py

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, db: Session, request):

        user = User(
            full_name=request.full_name,
            password=hash_password(request.password),
            gender=request.gender,
            role_id=request.role_id,
            apartment_id=request.apartment_id,
            status="ACTIVE"
        )

        created_user = self.user_repository.create(db, user)

        return created_user
