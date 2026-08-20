from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CreateSubscriptionRequest(BaseModel):
    apartment_id: int
    plan_code: str


class SubscriptionResponse(BaseModel):
    id: int
    apartment_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    amount: Decimal
    status: str

    model_config = ConfigDict(from_attributes=True)