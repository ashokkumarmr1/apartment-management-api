from sqlalchemy.orm import Session

from app.models.visitor import Visitor
from app.repositories.base_repository import BaseRepository


class VisitorRepository(
    BaseRepository[Visitor]
):

    def __init__(self):
        super().__init__(Visitor)

    def get_by_id_and_apartment(
        self,
        db: Session,
        visitor_id: int,
        apartment_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.id == visitor_id,
                self.model.apartment_id == apartment_id,
            )
            .first()
        )

    def get_all_by_apartment(
        self,
        db: Session,
        apartment_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.apartment_id == apartment_id,
            )
            .order_by(
                self.model.created_at.desc()
            )
            .all()
        )

    def get_active_by_apartment(
        self,
        db: Session,
        apartment_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.apartment_id == apartment_id,
                self.model.status.in_([
                    "EXPECTED",
                    "CHECKED_IN",
                ]),
            )
            .order_by(
                self.model.created_at.desc()
            )
            .all()
        )