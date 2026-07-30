from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.role_repository import RoleRepository


class RoleService:

    DEFAULT_ROLES = [
        ("Super Admin", "SUPER_ADMIN"),
        ("Apartment Admin", "APARTMENT_ADMIN"),
        ("Owner", "OWNER"),
        ("Tenant", "TENANT"),
        ("Security", "SECURITY"),
        ("Maintenance", "MAINTENANCE"),
    ]

    @staticmethod
    def seed_roles(db: Session):

        for name, code in RoleService.DEFAULT_ROLES:

            role = RoleRepository.get_by_code(db, code)

            if role:
                continue

            RoleRepository.create(
                db,
                Role(
                    name=name,
                    code=code
                )
            )

        print("Default Roles Ready")