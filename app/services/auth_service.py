# app/services/auth_service.py

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, db: Session, request):

        existing_user = self.user_repository.get_by_mobile(
            db,
            request.mobile
        )

        if existing_user:
            raise ValueError("Mobile number already registered.")

        user = User(
            full_name=request.full_name,
            mobile=request.mobile,
            password=hash_password(request.password),
            gender=request.gender,
            role_id=request.role_id,
            apartment_id=request.apartment_id,
            status="ACTIVE"
        )

        return self.user_repository.create(db, user)

    def login(self, db: Session, request):

        user = self.user_repository.get_by_mobile(
            db,
            request.mobile
        )

        if not user:
            raise ValueError("Invalid mobile or password.")

        if not verify_password(
                request.password,
                user.password
        ):
            raise ValueError("Invalid mobile or password.")

        token = create_access_token(
            {
                "sub": str(user.id),
                "mobile": user.mobile,
                "role_id": user.role_id
            }
        )

        return {
            "user": user,
            "access_token": token
        }