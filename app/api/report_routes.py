from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import RentObligationResponse
from app.services.report_services import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/overdue-rent",
    response_model=list[RentObligationResponse]
)
def overdue_rent(
    db: Session = Depends(get_db)
):
    return ReportService(db).overdue_rent()