from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateVisitorRequest(BaseModel):
    visitor_name: str
    mobile: str
    vehicle_number: str | None = None
    visitor_type: str
    purpose: str | None = None
    expected_date: datetime | None = None


class UpdateVisitorRequest(BaseModel):
    visitor_name: str | None = None
    mobile: str | None = None
    vehicle_number: str | None = None
    visitor_type: str | None = None
    purpose: str | None = None
    expected_date: datetime | None = None


class VisitorResponse(BaseModel):
    id: int
    apartment_id: int
    created_by: int
    visitor_name: str
    mobile: str
    vehicle_number: str | None
    visitor_type: str
    purpose: str | None
    expected_date: datetime | None
    check_in_time: datetime | None
    check_out_time: datetime | None
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )