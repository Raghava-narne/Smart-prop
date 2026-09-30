from datetime import date

from app.models.tenant import Tenant
from app.repositories.tenant_repo import TenantRepository
from app.core.exceptions import AppError


class TenantService:

    def __init__(self, db):
        self.repo = TenantRepository(db)

    def create(self, data):
        if self.repo.by_email(str(data.email)):
            raise AppError(
                "Tenant email already exists",
                409
            )

        values = data.model_dump()

        values["registration_date"] = date.today()
        values["status"] = values.get("status") or "ACTIVE"

        return self.repo.add(
            Tenant(**values)
        )

    def list(self):
        return self.repo.list()

    def get(self, tenant_id):
        obj = self.repo.get(tenant_id)

        if not obj:
            raise AppError(
                "Tenant not found",
                404
            )

        return obj

    def update(self, tenant_id, data):
        obj = self.get(tenant_id)

        values = data.model_dump(
            exclude_unset=True
        )

        for key, value in values.items():
            if value is not None:
                setattr(obj, key, value)

        self.repo.db.commit()
        self.repo.db.refresh(obj)

        return obj

    def deactivate(self, tenant_id):
        obj = self.get(tenant_id)

        obj.status = "INACTIVE"

        self.repo.db.commit()
        self.repo.db.refresh(obj)

        return obj