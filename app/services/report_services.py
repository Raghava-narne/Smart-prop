from app.repositories.rent_repo import RentObligationRepository


class ReportService:

    def __init__(self, db):
        self.repo = RentObligationRepository(db)

    def overdue_rent(self):
        rents = self.repo.list()

        return [
            rent
            for rent in rents
            if rent.status == "OVERDUE"
        ]