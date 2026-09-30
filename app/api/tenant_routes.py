from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import TenantCreate, TenantUpdate, TenantResponse
from app.services.tenant_services import TenantService
router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.post("", response_model=TenantResponse, status_code=201)
def create_tenant(data: TenantCreate, db: Session = Depends(get_db)):
    return TenantService(db).create(data)


@router.get("", response_model=list[TenantResponse])
def list_tenants(db: Session = Depends(get_db)):
    return TenantService(db).list()


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return TenantService(db).get(tenant_id)


@router.patch("/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: int, data: TenantUpdate, db: Session = Depends(get_db)):
    return TenantService(db).update(tenant_id, data)


@router.patch("/{tenant_id}/deactivate", response_model=TenantResponse)
def deactivate_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return TenantService(db).deactivate(tenant_id)
