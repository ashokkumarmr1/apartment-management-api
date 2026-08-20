from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.subscription import (
    CreateSubscriptionRequest,
    SubscriptionResponse,
    UpdateSubscriptionRequest,
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
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_subscription( 
            db,
            current_user.apartment_id,
            request.plan_code,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=SubscriptionResponse,
)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription = service.get_active_subscription(
        db,
        current_user.apartment_id,
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found.",
        )

    return subscription

@router.put(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
def update_subscription(
    subscription_id: int,
    request: UpdateSubscriptionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.update_subscription(
            db,
            subscription_id,
            current_user.apartment_id,
            request.plan_code,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.delete(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.cancel_subscription(
            db,
            subscription_id,
            current_user.apartment_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )