from typing import Any

from app.core.exceptions import AuditNotFoundError
from app.domain.interfaces.audit_repository import AuditRepository


class AuditService:
    """Caso de uso: consulta do histórico de auditorias."""

    def __init__(self, repository: AuditRepository):
        self._repository = repository

    def list_audits(self, skip: int, limit: int) -> list[Any]:
        return self._repository.list(skip, limit)

    def get_audit(self, audit_id: int) -> Any:
        record = self._repository.get(audit_id)
        if not record:
            raise AuditNotFoundError("Auditoria não encontrada")
        return record
