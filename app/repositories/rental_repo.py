from sqlalchemy.orm import Session

from app.models.rental_agreement import RentalAgreement


class RentalAgreementRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, agreement: RentalAgreement):
        self.db.add(agreement)
        self.db.commit()
        self.db.refresh(agreement)
        return agreement

    def list(self):
        return self.db.query(RentalAgreement).all()

    def get(self, agreement_id: int):
        return (
            self.db.query(RentalAgreement)
            .filter(
                RentalAgreement.agreement_id == agreement_id
            )
            .first()
        )

    def by_tenant(self, tenant_id: int):
        return (
            self.db.query(RentalAgreement)
            .filter(
                RentalAgreement.tenant_id == tenant_id
            )
            .all()
        )

    def by_apartment(self, apartment_id: int):
        return (
            self.db.query(RentalAgreement)
            .filter(
                RentalAgreement.apartment_id == apartment_id
            )
            .all()
        )

    def active_for_apartment(self, apartment_id: int):
        return (
            self.db.query(RentalAgreement)
            .filter(
                RentalAgreement.apartment_id == apartment_id,
                RentalAgreement.status == "ACTIVE"
            )
            .all()
        )

    def current_for_apartment(self, apartment_id: int):
        return (
            self.db.query(RentalAgreement)
            .filter(
                RentalAgreement.apartment_id == apartment_id,
                RentalAgreement.status == "ACTIVE"
            )
            .order_by(
                RentalAgreement.start_date.desc()
            )
            .first()
        )

