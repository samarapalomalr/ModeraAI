"""Dependências injetadas nas rotas."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.audit_service import AuditService


def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)
