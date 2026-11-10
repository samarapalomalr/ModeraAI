from typing import Optional

from sqlalchemy.orm import Session

from app.domain.interfaces.audit_repository import AuditRepository
from app.infrastructure.database.models import Audit


class SqlAlchemyAuditRepository(AuditRepository):
    def __init__(self, db: Session):
        self._db = db

    def list(self, skip: int, limit: int) -> list[Audit]:
        return (
            self._db.query(Audit)
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, audit_id: int) -> Optional[Audit]:
        return self._db.query(Audit).filter(Audit.id == audit_id).first()

    def save(
        self,
        platform: str,
        target_url: str,
        raw_content: Optional[str],
        summary: Optional[str],
        compliance_score: Optional[int],
        result_json: str,
        status: str = "COMPLETED",
    ) -> Audit:
        audit = Audit(
            platform=platform,
            target_url=target_url,
            raw_content=raw_content,
            summary=summary,
            compliance_score=compliance_score,
            result_json=result_json,
            status=status,
        )
        self._db.add(audit)
        self._db.commit()
        self._db.refresh(audit)
        return audit
