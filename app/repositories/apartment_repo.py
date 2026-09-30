from sqlalchemy.orm import Session

from app.models.apartment import Apartment


class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, apartment: Apartment):
        self.db.add(apartment)
        self.db.commit()
        self.db.refresh(apartment)
        return apartment

    def list(self):
        return self.db.query(Apartment).all()

    def get(self, apartment_id: int):
        return (
            self.db.query(Apartment)
            .filter(Apartment.apartment_id == apartment_id)
            .first()
        )

    def by_property(self, property_id: int):
        return (
            self.db.query(Apartment)
            .filter(Apartment.property_id == property_id)
            .all()
        )

    def by_property_and_number(
        self,
        property_id: int,
        apartment_number: str
    ):
        return (
            self.db.query(Apartment)
            .filter(
                Apartment.property_id == property_id,
                Apartment.apartment_number == apartment_number
            )
            .first()
        )