"""Regras de negócio do histórico de auditorias."""
from sqlalchemy.orm import Session

from app.core.exceptions import AuditNotFoundError
from app.models.audit import Audit
from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db: Session):
        self.repository = AuditRepository(db)

    def list_audits(self, skip: int = 0, limit: int = 20) -> list[Audit]:
        return self.repository.list(skip=skip, limit=limit)

    def get_audit(self, audit_id: int) -> Audit:
        audit = self.repository.get_by_id(audit_id)
        if not audit:
            raise AuditNotFoundError("Auditoria não encontrada")
        return audit
