"""Camada de acesso a dados: única que conhece SQLAlchemy/Session."""
from sqlalchemy.orm import Session

from app.models.audit import Audit


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 20) -> list[Audit]:
        return (
            self.db.query(Audit)
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, audit_id: int) -> Audit | None:
        return self.db.query(Audit).filter(Audit.id == audit_id).first()
