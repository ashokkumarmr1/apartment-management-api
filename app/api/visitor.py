from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
)
from app.models.user import User

from app.schemas.visitor import (
    CreateVisitorRequest,
    UpdateVisitorRequest,
    VisitorResponse,
)
from app.services.visitor_service import (
    VisitorService,
)


router = APIRouter(
    prefix="/visitors",
    tags=["Visitors"],
)

service = VisitorService()


@router.post(
    "",
    response_model=VisitorResponse,
    status_code=201,
)
def create_visitor(
    request: CreateVisitorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        return service.create_visitor(
            db=db,
            apartment_id=current_user.apartment_id,
            user_id=current_user.id,
            visitor_name=request.visitor_name,
            mobile=request.mobile,
            vehicle_number=request.vehicle_number,
            visitor_type=request.visitor_type,
            purpose=request.purpose,
            expected_date=request.expected_date,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get(
    "",
    response_model=list[VisitorResponse],
)
def get_visitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_visitors(
        db,
        current_user.apartment_id,
    )


@router.get(
    "/{visitor_id}",
    response_model=VisitorResponse,
)
def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.get_visitor(
            db=db,
            visitor_id=visitor_id,
            apartment_id=current_user.apartment_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/{visitor_id}/check-in",
    response_model=VisitorResponse,
)
def check_in_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        return service.check_in_visitor(
            db=db,
            visitor_id=visitor_id,
            apartment_id=current_user.apartment_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post(
    "/{visitor_id}/check-out",
    response_model=VisitorResponse,
)
def check_out_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        return service.check_out_visitor(
            db=db,
            visitor_id=visitor_id,
            apartment_id=current_user.apartment_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.put(
    "/{visitor_id}",
    response_model=VisitorResponse,
)
def update_visitor(
    visitor_id: int,
    request: UpdateVisitorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        return service.update_visitor(
            db=db,
            visitor_id=visitor_id,
            apartment_id=current_user.apartment_id,
            data=request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.delete(
    "/{visitor_id}",
    status_code=204,
)
def delete_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        service.delete_visitor(
            db=db,
            visitor_id=visitor_id,
            apartment_id=current_user.apartment_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )