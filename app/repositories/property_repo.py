from sqlalchemy.orm import Session

from app.models.property import Property


class PropertyRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, property_obj: Property):
        self.db.add(property_obj)
        self.db.commit()
        self.db.refresh(property_obj)
        return property_obj

    def list(self):
        return self.db.query(Property).all()

    def get(self, property_id: int):
        return (
            self.db.query(Property)
            .filter(Property.property_id == property_id)
            .first()
        )

    def update(self, property_obj: Property):
        self.db.commit()
        self.db.refresh(property_obj)
        return property_obj

    def delete(self, property_obj: Property):
        self.db.delete(property_obj)
        self.db.commit()