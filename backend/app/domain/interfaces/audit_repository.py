from abc import ABC, abstractmethod
from typing import Any, Optional


class AuditRepository(ABC):
    """Contrato de leitura do histórico de auditorias."""

    @abstractmethod
    def list(self, skip: int, limit: int) -> list[Any]: ...

    @abstractmethod
    def get(self, audit_id: int) -> Optional[Any]: ...

    @abstractmethod
    def save(
        self,
        platform: str,
        target_url: str,
        raw_content: Optional[str],
        summary: Optional[str],
        compliance_score: Optional[int],
        result_json: str,
        status: str = "COMPLETED",
    ) -> Any: ...
