from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):

    def __init__(self):
        super().__init__(Role)

    def get_by_code(
        self,
        db: Session,
        code: str,
    ) -> Role | None:

        return (
            db.query(Role)
            .filter(Role.code == code)
            .first()
        )