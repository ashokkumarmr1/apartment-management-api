from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.subscription_plan_repository import (
    SubscriptionPlanRepository,
)


class SubscriptionService:

    def __init__(self):
        self.subscription_repository = SubscriptionRepository()
        self.plan_repository = SubscriptionPlanRepository()

    def create_subscription(
        self,
        db: Session,
        apartment_id: int,
        plan_code: str,
    ) -> Subscription:

        # Find subscription plan
        plan = self.plan_repository.get_by_code(
            db,
            plan_code,
        )

        if plan is None:
            raise ValueError(
                "Subscription plan not found."
            )

        if not plan.is_active:
            raise ValueError(
                "Subscription plan is inactive."
            )

        # Check existing active subscription
        existing = (
            self.subscription_repository
            .get_active_by_apartment(
                db,
                apartment_id,
            )
        )

        if existing:
            raise ValueError(
                "Apartment already has an active subscription."
            )

        start_date = datetime.utcnow()

        end_date = (
            start_date
            + timedelta(
                days=plan.duration_days
            )
        )

        subscription = Subscription(
            apartment_id=apartment_id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            amount=plan.price,
            status="ACTIVE",
        )

        return self.subscription_repository.create(
            db,
            subscription,
        )

    def get_active_subscription(
        self,
        db: Session,
        apartment_id: int,
    ):

        subscription = (
            self.subscription_repository
            .get_active_by_apartment(
                db,
                apartment_id,
            )
        )

        if subscription is None:
            return None

        # Automatically expire subscription
        if subscription.end_date <= datetime.utcnow():

            subscription.status = "EXPIRED"

            self.subscription_repository.update(
                db,
                subscription,
            )

            return None

        return subscription

    def is_subscription_active(
        self,
        db: Session,
        apartment_id: int,
    ) -> bool:

        subscription = self.get_active_subscription(
            db,
            apartment_id,
        )

        return subscription is not None

    def cancel_subscription(
            self,
            db: Session,
            subscription_id: int,
            apartment_id: int,
    ) -> Subscription:

        subscription = (
            self.subscription_repository
            .get_by_id_and_apartment(
                db,
                subscription_id,
                apartment_id,
            )
        )

        if subscription is None:
            raise ValueError(
                "Subscription not found."
            )

        if subscription.status != "ACTIVE":
            raise ValueError(
                "Only active subscriptions can be cancelled."
            )

        subscription.status = "CANCELLED"

        return self.subscription_repository.update(
            db,
            subscription,
        )

    def update_subscription(
            self,
            db: Session,
            subscription_id: int,
            apartment_id: int,
            plan_code: str,
    ) -> Subscription:

        subscription = (
            self.subscription_repository
            .get_by_id_and_apartment(
                db,
                subscription_id,
                apartment_id,
            )
        )

        if subscription is None:
            raise ValueError(
                "Subscription not found."
            )

        if subscription.status != "ACTIVE":
            raise ValueError(
                "Only active subscriptions can be updated."
            )

        plan = self.plan_repository.get_by_code(
            db,
            plan_code,
        )

        if plan is None:
            raise ValueError(
                "Subscription plan not found."
            )

        if not plan.is_active:
            raise ValueError(
                "Subscription plan is inactive."
            )

        subscription.plan_id = plan.id
        subscription.amount = plan.price

        subscription.end_date = (
                subscription.start_date
                + timedelta(days=plan.duration_days)
        )

        return self.subscription_repository.update(
            db,
            subscription,
        )