from sqlalchemy.orm import Session
from datetime import datetime, UTC

from app.models.visitor import Visitor
from app.repositories.visitor_repository import (
    VisitorRepository,
)


class VisitorService:

    ALLOWED_VISITOR_TYPES = {
        "GUEST",
        "DELIVERY",
        "CAB",
        "SERVICE",
        "VENDOR",
        "OTHER",
    }

    def __init__(self):
        self.repository = VisitorRepository()

    def create_visitor(
        self,
        db: Session,
        apartment_id: int,
        user_id: int,
        visitor_name: str,
        mobile: str,
        vehicle_number: str | None,
        visitor_type: str,
        purpose: str | None,
        expected_date,
    ) -> Visitor:

        visitor_type = visitor_type.upper()

        if visitor_type not in self.ALLOWED_VISITOR_TYPES:
            raise ValueError(
                "Invalid visitor type."
            )

        visitor = Visitor(
            apartment_id=apartment_id,
            created_by=user_id,
            visitor_name=visitor_name,
            mobile=mobile,
            vehicle_number=vehicle_number,
            visitor_type=visitor_type,
            purpose=purpose,
            expected_date=expected_date,
            status="EXPECTED",
        )

        return self.repository.create(
            db,
            visitor,
        )

    def get_visitors(
            self,
            db: Session,
            apartment_id: int,
    ):
        return self.repository.get_all_by_apartment(
            db,
            apartment_id,
        )

    def get_visitor(
            self,
            db: Session,
            visitor_id: int,
            apartment_id: int,
    ):
        visitor = self.repository.get_by_id_and_apartment(
            db,
            visitor_id,
            apartment_id,
        )

        if visitor is None:
            raise ValueError(
                "Visitor not found."
            )

        return visitor

    def check_in_visitor(
            self,
            db: Session,
            visitor_id: int,
            apartment_id: int,
    ):
        visitor = self.repository.get_by_id_and_apartment(
            db,
            visitor_id,
            apartment_id,
        )

        if visitor is None:
            raise ValueError(
                "Visitor not found."
            )

        if visitor.status == "CHECKED_IN":
            raise ValueError(
                "Visitor is already checked in."
            )

        if visitor.status == "CHECKED_OUT":
            raise ValueError(
                "Visitor has already checked out."
            )

        if visitor.status != "EXPECTED":
            raise ValueError(
                "Visitor cannot be checked in."
            )

        visitor.status = "CHECKED_IN"
        visitor.check_in_time = datetime.now(UTC)

        return self.repository.update(
            db,
            visitor,
        )

    def check_out_visitor(
            self,
            db: Session,
            visitor_id: int,
            apartment_id: int,
    ):
        visitor = self.repository.get_by_id_and_apartment(
            db,
            visitor_id,
            apartment_id,
        )

        if visitor is None:
            raise ValueError(
                "Visitor not found."
            )

        if visitor.status == "EXPECTED":
            raise ValueError(
                "Visitor has not checked in."
            )

        if visitor.status == "CHECKED_OUT":
            raise ValueError(
                "Visitor is already checked out."
            )

        if visitor.status != "CHECKED_IN":
            raise ValueError(
                "Visitor cannot be checked out."
            )

        visitor.status = "CHECKED_OUT"
        visitor.check_out_time = datetime.now(UTC)

        return self.repository.update(
            db,
            visitor,
        )

    def update_visitor(
            self,
            db: Session,
            visitor_id: int,
            apartment_id: int,
            data,
    ):
        visitor = self.repository.get_by_id_and_apartment(
            db,
            visitor_id,
            apartment_id,
        )

        if visitor is None:
            raise ValueError(
                "Visitor not found."
            )

        if visitor.status != "EXPECTED":
            raise ValueError(
                "Only expected visitors can be updated."
            )

        if data.visitor_name is not None:
            visitor.visitor_name = data.visitor_name

        if data.mobile is not None:
            visitor.mobile = data.mobile

        if data.vehicle_number is not None:
            visitor.vehicle_number = data.vehicle_number

        if data.visitor_type is not None:

            visitor_type = data.visitor_type.upper()

            if visitor_type not in self.ALLOWED_VISITOR_TYPES:
                raise ValueError(
                    "Invalid visitor type."
                )

            visitor.visitor_type = visitor_type

        if data.purpose is not None:
            visitor.purpose = data.purpose

        if data.expected_date is not None:
            visitor.expected_date = data.expected_date

        return self.repository.update(
            db,
            visitor,
        )

    def delete_visitor(
            self,
            db: Session,
            visitor_id: int,
            apartment_id: int,
    ):
        visitor = self.repository.get_by_id_and_apartment(
            db,
            visitor_id,
            apartment_id,
        )

        if visitor is None:
            raise ValueError(
                "Visitor not found."
            )

        if visitor.status != "EXPECTED":
            raise ValueError(
                "Only expected visitors can be deleted."
            )

        self.repository.delete(
            db,
            visitor,
        )