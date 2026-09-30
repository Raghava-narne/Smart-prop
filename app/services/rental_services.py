from app.models.rental_agreement import RentalAgreement
from app.repositories.rental_repo import RentalAgreementRepository
from app.repositories.tenant_repo import TenantRepository
from app.repositories.apartment_repo import ApartmentRepository
from app.core.exceptions import AppError
from app.services.audit_services import AuditService


class RentalService:
    def __init__(self, db):
        self.repo = RentalAgreementRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.apartment_repo = ApartmentRepository(db)
        self.audit = AuditService(db)

    def create(self, data):
        tenant = self.tenant_repo.get(data.tenant_id)
        apartment = self.apartment_repo.get(data.apartment_id)

        if not tenant:
            raise AppError("Tenant not found", 404)

        if not apartment:
            raise AppError("Apartment not found", 404)

        if tenant.status != "ACTIVE":
            raise AppError("Inactive tenant cannot create a rental agreement")

        if apartment.status != "AVAILABLE":
            raise AppError("Apartment is not available")

        if data.end_date <= data.start_date:
            raise AppError("Agreement end date must be after date")

        for existing in self.repo.active_for_apartment(data.apartment_id):
            if (
                data.start_date < existing.end_date
                and data.end_date > existing.start_date
            ):
                raise AppError(
                    "Rental agreement overlaps an active agreement",
                    409
                )

        values = data.model_dump()
        values["status"] = data.status or "ACTIVE"

        obj = self.repo.add(RentalAgreement(**values))

        if obj.status == "ACTIVE":
            apartment.status = "OCCUPIED"
            self.repo.db.commit()
            self.repo.db.refresh(obj)

        # Automatic audit after successful rental agreement creation
        self.audit.log_event(
            event_type="RENTAL_AGREEMENT_CREATED",
            entity_type="RENTAL_AGREEMENT",
            entity_id=obj.agreement_id,
            actor_reference=None,
            metadata={
                "tenant_id": obj.tenant_id,
                "apartment_id": obj.apartment_id,
                "status": obj.status
            }
        )

        return obj

    def list(self):
        return self.repo.list()

    def get(self, agreement_id):
        obj = self.repo.get(agreement_id)

        if not obj:
            raise AppError("Rental agreement not found", 404)

        return obj

    def terminate(self, agreement_id):
        obj = self.get(agreement_id)

        obj.status = "TERMINATED"

        apartment = self.apartment_repo.get(obj.apartment_id)

        if apartment:
            apartment.status = "AVAILABLE"

        self.repo.db.commit()
        self.repo.db.refresh(obj)

        # Automatic audit after successful rental agreement termination
        self.audit.log_event(
            event_type="RENTAL_AGREEMENT_TERMINATED",
            entity_type="RENTAL_AGREEMENT",
            entity_id=obj.agreement_id,
            actor_reference=None,
            metadata={
                "tenant_id": obj.tenant_id,
                "apartment_id": obj.apartment_id,
                "status": obj.status
            }
        )

        return obj

    def current_tenant(self, apartment_id):
        agreement = self.repo.current_for_apartment(apartment_id)

        if not agreement:
            return None

        return self.tenant_repo.get(agreement.tenant_id)

