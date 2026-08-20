from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.repositories.base_repository import BaseRepository


class SubscriptionRepository(
    BaseRepository[Subscription]
):

    def __init__(self):
        super().__init__(Subscription)

    def get_active_by_apartment(
        self,
        db: Session,
        apartment_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.apartment_id == apartment_id,
                self.model.status == "ACTIVE",
            )
            .first()
        )

    def get_latest_by_apartment(
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
            .first()
        )

    def get_by_id_and_apartment(
            self,
            db: Session,
            subscription_id: int,
            apartment_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.id == subscription_id,
                self.model.apartment_id == apartment_id,
            )
            .first()
        )