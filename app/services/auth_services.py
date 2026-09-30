from app.core.exceptions import AppError
from app.core.security import hash_password, verify_password
from app.repositories.user_repo import UserRepository
from app.models.user import User


class AuthService:

    def __init__(self, db):
        self.repo = UserRepository(db)

    def authenticate(
        self,
        email: str,
        password: str
    ):
        user = self.repo.by_email(email)

        if not user:
            raise AppError(
                "Invalid email or password",
                401
            )

        if not verify_password(
            password,
            user.password
        ):
            raise AppError(
                "Invalid email or password",
                401
            )

        if user.status != "active":
            raise AppError(
                "User is inactive",
                403
            )

        return user

    def register(self, data):
        existing_user = self.repo.by_email(str(data.email))

        if existing_user:
            raise AppError(
                "Email already registered",
                409
            )

        hashed_password = hash_password(data.password)

        user = User(
            full_name=data.full_name,
            email=str(data.email),
            password=hashed_password,
            role_id=data.role_id,
            status="active"
        )

        return self.repo.add(user)

