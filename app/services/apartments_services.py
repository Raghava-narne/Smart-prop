from app.models.apartment import Apartment
from app.repositories.apartment_repo import ApartmentRepository
from app.repositories.property_repo import PropertyRepository
from app.core.exceptions import AppError


class ApartmentService:
    def __init__(self, db):
        self.repo = ApartmentRepository(db)
        self.property_repo = PropertyRepository(db)

    def create(self, property_id: int, data):
        if not self.property_repo.get(property_id):
            raise AppError("Property not found", 404)

        if data.monthly_rent <= 0:
            raise AppError("Monthly rent must be greater than zero")

        if self.repo.by_property_and_number(property_id, data.apartment_number):
            raise AppError("Apartment number must be unique within a property")

        values = data.model_dump()
        values["property_id"] = property_id
        obj = Apartment(**values)
        return self.repo.add(obj)

    def list_by_property(self, property_id):
        if not self.property_repo.get(property_id):
            raise AppError("Property not found", 404)
        return self.repo.by_property(property_id)

    def get(self, apartment_id):
        obj = self.repo.get(apartment_id)
        if not obj:
            raise AppError("Apartment not found", 404)
        return obj

    def update(self, apartment_id, data):
        obj = self.get(apartment_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(obj, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(obj)
        return obj

    def filter_by_status(self, status):
        return [
            apartment for apartment in self.repo.list()
            if apartment.status == status
        ]
