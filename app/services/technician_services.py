from app.models.technician import Technician
from app.repositories.technician_repo import TechnicianRepository
from app.core.exceptions import AppError


class TechnicianService:

    def __init__(self, db):
        self.repo = TechnicianRepository(db)

    def create(self, data):
        values = data.model_dump()

        values["availability_status"] = (
            values.get("availability_status")
            or "AVAILABLE"
        )

        technician = Technician(**values)

        return self.repo.add(technician)

    def list(self):
        return self.repo.list()

    def get(self, technician_id):
        technician = self.repo.get(technician_id)

        if not technician:
            raise AppError(
                "Technician not found",
                404
            )

        return technician

    def update(self, technician_id, data):
        technician = self.repo.get(technician_id)

        if not technician:
            raise AppError(
                "Technician not found",
                404
            )

        return self.repo.update(
            technician_id,
            data
        )