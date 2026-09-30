from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.audit_services import AuditService
router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("")
def list_audit_events(db: Session = Depends(get_db)):
    return AuditService(db).list()
