# app/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
