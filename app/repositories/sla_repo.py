from sqlalchemy.orm import Session

from app.models.sla_policy import SLAPolicy


class SLAPolicyRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, policy: SLAPolicy):

        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)

        return policy

    def list(self):

        return (
            self.db
            .query(SLAPolicy)
            .order_by(SLAPolicy.sla_id)
            .all()
        )

    def get(self, sla_id: int):

        return (
            self.db
            .query(SLAPolicy)
            .filter(
                SLAPolicy.sla_id == sla_id
            )
            .first()
        )

    def get_by_priority(self, priority: str):

        return (
            self.db
            .query(SLAPolicy)
            .filter(
                SLAPolicy.priority == priority
            )
            .first()
        )

    def update(self, policy: SLAPolicy):

        self.db.commit()
        self.db.refresh(policy)

        return policy