from app.models.audit_log import AuditLog
from app.repositories.audit_repo import AuditLogRepository


class AuditService:
    def __init__(self, db):
        self.repo = AuditLogRepository(db)

    def log_event(
        self,
        event_type: str,
        entity_type: str,
        entity_id: int,
        actor_reference: str | None,
        metadata: dict | None = None,
    ):
        event = AuditLog(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            actor_reference=actor_reference,
            metadata_json=metadata,
        )
        return self.repo.add(event)

    def list(self):
        return self.repo.list()
