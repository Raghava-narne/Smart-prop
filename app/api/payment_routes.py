from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import (
    PaymentCreate,
    PaymentResponse,
    RazorpayOrderCreate,
    RazorpayOrderResponse,
    RazorpayPaymentVerification,
)
from app.services.paymentservices import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse, status_code=201)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService(db).create(data)


@router.post("/razorpay/orders", response_model=RazorpayOrderResponse, status_code=201)
def create_razorpay_order(data: RazorpayOrderCreate, db: Session = Depends(get_db)):
    return PaymentService(db).create_razorpay_order(data)


@router.post("/razorpay/verify", response_model=PaymentResponse)
def verify_razorpay_payment(
    data: RazorpayPaymentVerification,
    db: Session = Depends(get_db),
):
    return PaymentService(db).verify_razorpay_payment(data)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return PaymentService(db).get(payment_id)

