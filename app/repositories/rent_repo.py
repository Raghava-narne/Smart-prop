from sqlalchemy.orm import Session

from app.models.rent_obligation import RentObligation
from app.models.rental_agreement import RentalAgreement


class RentObligationRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, rent: RentObligation):
        self.db.add(rent)
        self.db.commit()
        self.db.refresh(rent)
        return rent

    def list(self):
        return self.db.query(RentObligation).all()

    def get(self, rent_id: int):
        return (
            self.db.query(RentObligation)
            .filter(RentObligation.rent_id == rent_id)
            .first()
        )

    def by_agreement(self, agreement_id: int):
        return (
            self.db.query(RentObligation)
            .filter(RentObligation.agreement_id == agreement_id)
            .all()
        )

    def by_agreement_and_month(
        self,
        agreement_id: int,
        billing_month
    ):
        return (
            self.db.query(RentObligation)
            .filter(
                RentObligation.agreement_id == agreement_id,
                RentObligation.billing_month == billing_month
            )
            .first()
        )

    def by_tenant(self, tenant_id: int):
        return (
            self.db.query(RentObligation)
            .join(
                RentalAgreement,
                RentObligation.agreement_id == RentalAgreement.agreement_id
            )
            .filter(
                RentalAgreement.tenant_id == tenant_id
            )
            .all()
        )