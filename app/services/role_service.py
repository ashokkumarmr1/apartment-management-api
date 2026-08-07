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

    role_repository = RoleRepository()

    @staticmethod
    def seed_roles(db: Session):

        for name, code in RoleService.DEFAULT_ROLES:

            role = RoleService.role_repository.get_by_code(
                db,
                code,
            )

            if role:
                continue

            RoleService.role_repository.create(
                db,
                Role(
                    name=name,
                    code=code,
                ),
            )

        print("Default Roles Ready")