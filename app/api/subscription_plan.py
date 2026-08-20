from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.subscription_plan import SubscriptionPlanResponse
from app.services.subscription_plan_service import SubscriptionPlanService


router = APIRouter(
    prefix="/subscription-plans",
    tags=["Subscription Plans"],
)

service = SubscriptionPlanService()


@router.get(
    "",
    response_model=list[SubscriptionPlanResponse],
)
def get_subscription_plans(
    db: Session = Depends(get_db),
):
    return service.get_active_plans(db)


@router.get(
    "/{plan_id}",
    response_model=SubscriptionPlanResponse,
)
def get_subscription_plan(
    plan_id: int,
    db: Session = Depends(get_db),
):
    plan = service.get_plan_by_id(
        db,
        plan_id,
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found",
        )

    return plan