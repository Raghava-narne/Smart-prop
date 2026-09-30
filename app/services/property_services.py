from app.models.property import Property
from app.repositories.property_repo import PropertyRepository
from app.core.exceptions import AppError
from app.services.audit_services import AuditService


class PropertyService:

    def __init__(self, db):
        self.repo = PropertyRepository(db)
        self.audit = AuditService(db)

    def create(self, data):
        property_obj = Property(**data.model_dump())

        property_obj = self.repo.add(property_obj)

        self.audit.log_event(
            event_type="PROPERTY_CREATED",
            entity_type="PROPERTY",
            entity_id=property_obj.property_id,
            actor_reference=None,
            metadata={
                "property_name": getattr(property_obj, "property_name", None)
            }
        )

        return property_obj

    def list(self):
        return self.repo.list()

    def get(self, property_id):
        obj = self.repo.get(property_id)

        if not obj:
            raise AppError("Property not found", 404)

        return obj

    def update(self, property_id, data):
        property_obj = self.repo.get(property_id)

        if not property_obj:
            raise AppError("Property not found", 404)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(property_obj, field, value)

        property_obj = self.repo.update(property_obj)

        return property_obj

    def delete(self, property_id):
        property_obj = self.repo.get(property_id)

        if not property_obj:
            raise AppError("Property not found", 404)

        self.repo.delete(property_obj)

        return {
            "message": "Property deleted successfully"
        }