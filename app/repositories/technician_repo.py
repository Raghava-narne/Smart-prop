from sqlalchemy.orm import Session

from app.models.technician import Technician


class TechnicianRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, technician: Technician):
        self.db.add(technician)
        self.db.commit()
        self.db.refresh(technician)
        return technician

    def list(self):
        return (
            self.db.query(Technician)
            .all()
        )

    def get(self, technician_id: int):
        return (
            self.db.query(Technician)
            .filter(
                Technician.technician_id == technician_id
            )
            .first()
        )

    def update(self, technician_id: int, data):
        technician = self.get(technician_id)

        if not technician:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                setattr(technician, key, value)

        self.db.commit()
        self.db.refresh(technician)

        return technician