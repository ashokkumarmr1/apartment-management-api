# app/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db, user):
        db.commit()
        db.refresh(user)
        return user

    def get_by_mobile(self, db: Session, mobile: str):
        return db.query(User).filter(User.mobile == mobile).first()