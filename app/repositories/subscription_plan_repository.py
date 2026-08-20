from sqlalchemy.orm import Session

from app.models.subscription_plan import SubscriptionPlan
from app.repositories.base_repository import BaseRepository


class SubscriptionPlanRepository(
    BaseRepository[SubscriptionPlan]
):

    def __init__(self):
        super().__init__(SubscriptionPlan)

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return (
            db.query(self.model)
            .filter(self.model.code == code)
            .first()
        )

    def get_all_active(
        self,
        db: Session,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.is_active.is_(True)
            )
            .order_by(
                self.model.price.asc()
            )
            .all()
        )

    def get_all_plans(
        self,
        db: Session,
        active_only: bool = True,
    ) -> list[SubscriptionPlan]:

        query = db.query(self.model)

        if active_only:
            query = query.filter(
                self.model.is_active.is_(True)
            )

        return (
            query
            .order_by(self.model.price.asc())
            .all()
        )