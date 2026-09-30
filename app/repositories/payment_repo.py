from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, payment: Payment):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def list(self):
        return self.db.query(Payment).all()

    def get(self, payment_id: int):
        return (
            self.db.query(Payment)
            .filter(Payment.payment_id == payment_id)
            .first()
        )

    def by_gateway_order(self, order_id: str):
        return (
            self.db.query(Payment)
            .filter(Payment.razorpay_order_id == order_id)
            .first()
        )

    def by_rent(self, rent_id: int):
        return (
            self.db.query(Payment)
            .filter(Payment.rent_id == rent_id)
            .all()
        )