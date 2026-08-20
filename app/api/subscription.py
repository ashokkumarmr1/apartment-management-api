from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.subscription import (
    CreateSubscriptionRequest,
    SubscriptionResponse,
)
from app.services.subscription_service import SubscriptionService


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)

service = SubscriptionService()


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=201,
)
def create_subscription(
    request: CreateSubscriptionRequest,
    db: Session = Depends(get_db),
):
    try:
        return service.create_subscription(
            db,
            request.apartment_id,
            request.plan_code,
        )

    except ValueError as e:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )