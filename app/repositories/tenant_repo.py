from sqlalchemy.orm import Session

from app.models.tenant import Tenant


class TenantRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, tenant: Tenant):
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant

    def list(self):
        return self.db.query(Tenant).all()

    def get(self, tenant_id: int):
        return (
            self.db.query(Tenant)
            .filter(Tenant.tenant_id == tenant_id)
            .first()
        )

    def by_email(self, email: str):
        return (
            self.db.query(Tenant)
            .filter(Tenant.email == email)
            .first()
        )