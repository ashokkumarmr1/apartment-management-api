from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.subscription_plan import SubscriptionPlan
from app.repositories.subscription_plan_repository import (
    SubscriptionPlanRepository,
)


class SubscriptionPlanService:

    DEFAULT_PLANS = [
        {
            "name": "Trial",
            "code": "TRIAL",
            "description": "30-day trial plan",
            "price": Decimal("0.00"),
            "duration_days": 30,
            "max_users": 10,
        },
        {
            "name": "Basic",
            "code": "BASIC",
            "description": "Basic apartment management plan",
            "price": Decimal("499.00"),
            "duration_days": 30,
            "max_users": 100,
        },
        {
            "name": "Standard",
            "code": "STANDARD",
            "description": "Standard apartment management plan",
            "price": Decimal("999.00"),
            "duration_days": 30,
            "max_users": 300,
        },
        {
            "name": "Premium",
            "code": "PREMIUM",
            "description": "Premium apartment management plan",
            "price": Decimal("9999.00"),
            "duration_days": 365,
            "max_users": None,
        },
    ]

    def __init__(self):
        self.repository = SubscriptionPlanRepository()

    def seed_plans(self, db: Session):

        for plan_data in self.DEFAULT_PLANS:

            existing_plan = self.repository.get_by_code(
                db,
                plan_data["code"],
            )

            if existing_plan:
                continue

            plan = SubscriptionPlan(
                name=plan_data["name"],
                code=plan_data["code"],
                description=plan_data["description"],
                price=plan_data["price"],
                duration_days=plan_data["duration_days"],
                max_users=plan_data["max_users"],
                is_active=True,
            )

            self.repository.create(
                db,
                plan,
            )

        print("Default Subscription Plans Ready")