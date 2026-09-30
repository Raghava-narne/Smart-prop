from datetime import date
from decimal import Decimal
from uuid import uuid4

import razorpay

from app.core.config import settings
from app.models.payment import Payment
from app.repositories.payment_repo import PaymentRepository
from app.repositories.rent_repo import RentObligationRepository
from app.core.exceptions import AppError
from app.services.audit_services import AuditService


class PaymentService:
    def __init__(self, db):
        self.repo = PaymentRepository(db)
        self.rent_repo = RentObligationRepository(db)
        self.audit = AuditService(db)

    def create(self, data):
        rent = self.rent_repo.get(data.rent_id)

        if not rent:
            raise AppError("Rent obligation not found", 404)

        outstanding = rent.amount_due - rent.amount_paid

        if data.amount <= 0:
            raise AppError("Payment amount must be positive")

        if data.amount > outstanding:
            raise AppError("Payment cannot exceed outstanding amount")

        payment = self.repo.add(
            Payment(**data.model_dump())
        )

        rent.amount_paid += data.amount

        if rent.amount_paid >= rent.amount_due:
            rent.status = "PAID"
        else:
            rent.status = "PARTIALLY_PAID"

        self.repo.db.commit()
        self.repo.db.refresh(payment)

        # Automatic audit after successful payment recording
        self.audit.log_event(
            event_type="PAYMENT_RECORDED",
            entity_type="PAYMENT",
            entity_id=payment.payment_id,
            actor_reference=None,
            metadata={
                "rent_id": payment.rent_id,
                "amount": str(payment.amount),
                "payment_method": payment.payment_method,
                "status": payment.status
            }
        )

        return payment

    def get(self, payment_id):
        obj = self.repo.get(payment_id)

        if not obj:
            raise AppError("Payment not found", 404)

        return obj

    def create_razorpay_order(self, data):
        client = self._razorpay_client()

        rent = self.rent_repo.get(data.rent_id)

        if not rent:
            raise AppError("Rent obligation not found", 404)

        outstanding = rent.amount_due - rent.amount_paid

        pending_amount = sum(
            (
                payment.amount
                for payment in self.repo.by_rent(data.rent_id)
                if payment.status.upper() == "PENDING"
            ),
            Decimal("0.00"),
        )

        if data.amount <= 0:
            raise AppError("Payment amount must be positive")

        if data.amount > outstanding - pending_amount:
            raise AppError("Payment cannot exceed outstanding amount")

        amount_in_paise = int(data.amount * 100)

        receipt = f"rent-{data.rent_id}-{uuid4().hex[:12]}"

        try:
            order = client.order.create(
                data={
                    "amount": amount_in_paise,
                    "currency": "INR",
                    "receipt": receipt,
                }
            )
        except Exception as exc:
            raise AppError(
                "Unable to create Razorpay order",
                502
            ) from exc

        payment = self.repo.add(
            Payment(
                rent_id=data.rent_id,
                amount=data.amount,
                payment_date=date.today(),
                payment_method="Razorpay",
                reference_number=None,
                status="PENDING",
                razorpay_order_id=order["id"],
            )
        )

        return {
            "payment_id": payment.payment_id,
            "razorpay_key_id": settings.razorpay_key_id,
            "razorpay_order_id": order["id"],
            "amount": amount_in_paise,
            "currency": "INR",
        }

    def verify_razorpay_payment(self, data):
        client = self._razorpay_client()

        payment = self.repo.by_gateway_order(
            data.razorpay_order_id
        )

        if not payment:
            raise AppError(
                "Razorpay order not found",
                404
            )

        try:
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": data.razorpay_order_id,
                    "razorpay_payment_id": data.razorpay_payment_id,
                    "razorpay_signature": data.razorpay_signature,
                }
            )
        except Exception as exc:
            raise AppError(
                "Invalid Razorpay payment signature",
                400
            ) from exc

        try:
            gateway_payment = client.payment.fetch(
                data.razorpay_payment_id
            )
        except Exception as exc:
            raise AppError(
                "Unable to retrieve Razorpay payment",
                502
            ) from exc

        if (
            gateway_payment.get("order_id")
            != data.razorpay_order_id
            or gateway_payment.get("amount")
            != int(payment.amount * 100)
            or gateway_payment.get("currency") != "INR"
        ):
            raise AppError(
                "Razorpay payment does not match the order",
                400
            )

        if gateway_payment.get("status") != "captured":
            raise AppError(
                "Razorpay payment has not been captured",
                409
            )

        if payment.status.upper() == "PAID":

            if (
                payment.razorpay_payment_id
                != data.razorpay_payment_id
            ):
                raise AppError(
                    "Payment was already verified with another payment id",
                    409
                )

            return payment

        if payment.status.upper() != "PENDING":
            raise AppError(
                "Payment is not awaiting verification",
                409
            )

        rent = self.rent_repo.get(payment.rent_id)

        if not rent:
            raise AppError(
                "Rent obligation not found",
                404
            )

        outstanding = rent.amount_due - rent.amount_paid

        if payment.amount > outstanding:
            raise AppError(
                "Verified payment exceeds outstanding rent",
                409
            )

        payment.razorpay_order_id = data.razorpay_order_id
        payment.razorpay_payment_id = data.razorpay_payment_id
        payment.razorpay_signature = data.razorpay_signature

        payment.status = "PAID"
        payment.payment_date = date.today()

        rent.amount_paid += payment.amount

        if rent.amount_paid >= rent.amount_due:
            rent.status = "PAID"
        else:
            rent.status = "PARTIALLY_PAID"

        self.repo.db.commit()
        self.repo.db.refresh(payment)

        # Automatic audit after successful Razorpay payment verification
        self.audit.log_event(
            event_type="PAYMENT_RECORDED",
            entity_type="PAYMENT",
            entity_id=payment.payment_id,
            actor_reference=None,
            metadata={
                "rent_id": payment.rent_id,
                "amount": str(payment.amount),
                "payment_method": payment.payment_method,
                "status": payment.status,
                "razorpay_payment_id": payment.razorpay_payment_id
            }
        )

        return payment

    @staticmethod
    def _razorpay_client():

        if (
            not settings.razorpay_key_id
            or not settings.razorpay_key_secret
        ):
            raise AppError(
                "Razorpay credentials are not configured",
                503
            )

        return razorpay.Client(
            auth=(
                settings.razorpay_key_id,
                settings.razorpay_key_secret,
            )
        )
