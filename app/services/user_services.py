from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core.exceptions import AppError


class UserService:

    def __init__(self, db):
        self.repo = UserRepository(db)

    def create(self, data):
        if self.repo.by_email(str(data.email)):
            raise AppError(
                "User email already exists",
                409
            )

        values = data.model_dump()

        user = User(**values)

        return self.repo.add(user)

    def list(self):
        return self.repo.list()

    def get(self, user_id):
        obj = self.repo.get(user_id)

        if not obj:
            raise AppError(
                "User not found",
                404
            )

        return obj