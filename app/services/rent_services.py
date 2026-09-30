from app.models.rent_obligation import RentObligation
from app.repositories.rent_repo import RentObligationRepository
from app.repositories.rental_repo import RentalAgreementRepository
from app.core.exceptions import AppError
from app.services.audit_services import AuditService


class RentService:
    def __init__(self, db):
        self.repo = RentObligationRepository(db)
        self.agreement_repo = RentalAgreementRepository(db)
        self.audit = AuditService(db)

    def generate(self, data):
        agreement = self.agreement_repo.get(data.agreement_id)

        if not agreement:
            raise AppError("Rental agreement not found", 404)

        if self.repo.by_agreement_and_month(
            data.agreement_id, data.billing_month
        ):
            raise AppError("Rent obligation already exists", 409)

        values = data.model_dump()
        values["status"] = data.status or "PENDING"

        rent = self.repo.add(RentObligation(**values))

        self.audit.log_event(
            event_type="RENT_OBLIGATION_GENERATED",
            entity_type="RENT_OBLIGATION",
            entity_id=rent.rent_id,
            actor_reference=None,
            metadata={
                "agreement_id": rent.agreement_id,
                "billing_month": str(rent.billing_month),
                "amount_due": str(rent.amount_due),
                "status": rent.status
            }
        )

        return rent

    def update(self, rent_id, data):
        rent = self.repo.get(rent_id)

        if not rent:
            raise AppError("Rent obligation not found", 404)

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(rent, key, value)

        self.repo.db.commit()
        self.repo.db.refresh(rent)

        return rent

    def list(self):
        return self.repo.list()

    def tenant_rent(self, tenant_id):
        return self.repo.by_tenant(tenant_id)