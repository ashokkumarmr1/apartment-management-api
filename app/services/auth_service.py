# app/services/auth_service.py

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException, DuplicateMobileException
from app.core.security import Security
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.utils.constants import Roles
from app.schemas.user import UserLogin


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    def register(
        self,
        db: Session,
        request: RegisterRequest,
    ) -> User:

        # Check email
        if self.user_repository.get_by_email(db, request.email):
            raise DuplicateEmailException(
                "Email already exists.",
                status_code=409,
            )

        # Check mobile
        if self.user_repository.get_by_mobile(db, request.mobile):
            raise DuplicateMobileException("Mobile number already exists.", status_code=409)

        # Default role
        role = self.role_repository.get_by_code(
            db,
            Roles.OWNER,
        )

        if role is None:
            raise ValueError("Default role not found.")

        user = User(
            full_name=request.full_name,
            email=request.email,
            mobile=request.mobile,
            password_hash=Security.hash_password(
                request.password
            ),
            role_id=role.id,
            apartment_id=request.apartment_id,
        )

        return self.user_repository.create(
            db,
            user,
        )

    def login(
            self,
            db: Session,
            request: UserLogin,
    ):
        # Find user
        user = self.user_repository.get_by_mobile(
            db,
            request.mobile,
        )

        if user is None:
            raise ValueError("Invalid mobile or password.")

        print("USER FOUND:", user.id)

        # Verify password
        if not Security.verify_password(
                request.password,
                user.password_hash,
        ):
            raise ValueError("Invalid mobile or password.")

        print("PASSWORD VERIFIED")

        # Generate JWT
        access_token = Security.create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.code,
            }
        )

        print("TOKEN CREATED")

        return {
            "user": user,
            "access_token": access_token,
        }