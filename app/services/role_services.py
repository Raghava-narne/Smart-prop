from app.models.role import Role
from app.repositories.role_repo import RoleRepository
from app.core.exceptions import AppError


class RoleService:
    def __init__(self, db):
        self.repo = RoleRepository(db)

    def create(self, data):
        if self.repo.by_name(data.role_name):
            raise AppError("Role already exists", 409)
        return self.repo.add(Role(**data.model_dump()))

    def list(self):
        return self.repo.list()

    def get(self, role_id):
        obj = self.repo.get(role_id)
        if not obj:
            raise AppError("Role not found", 404)
        return obj

    def update(self, role_id, data):
        obj = self.get(role_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(obj, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(obj)
        return obj