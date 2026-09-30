from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    def list(self):
        return (
            self.db.query(User)
            .order_by(User.user_id)
            .all()
        )

    def add(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user