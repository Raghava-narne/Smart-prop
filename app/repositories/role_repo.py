from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, role: Role):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def list(self):
        return self.db.query(Role).all()

    def get(self, role_id: int):
        return (
            self.db.query(Role)
            .filter(Role.role_id == role_id)
            .first()
        )

    def by_name(self, role_name: str):
        return (
            self.db.query(Role)
            .filter(Role.role_name == role_name)
            .first()
        )