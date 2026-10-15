from decimal import Decimal
# todo
# dont include space in import area
from pydantic import BaseModel, ConfigDict


class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    price: Decimal
    duration_days: int
    max_users: int | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )