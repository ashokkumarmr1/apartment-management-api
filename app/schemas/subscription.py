from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
# todo
# dont include space in import area

class CreateSubscriptionRequest(BaseModel):
    plan_code: str


class UpdateSubscriptionRequest(BaseModel):
    plan_code: str


class SubscriptionResponse(BaseModel):
    id: int
    apartment_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    amount: Decimal
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )