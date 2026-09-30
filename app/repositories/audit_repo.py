from app.models.audit_log import AuditLog


class AuditLogRepository:

    def __init__(self, db):
        self.db = db

    def list(self):
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.timestamp.desc())
            .all()
        )

    def add(self, audit_log):
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log