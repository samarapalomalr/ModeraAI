from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_audit_service
from app.core.exceptions import AuditNotFoundError
from app.schemas.analyze import AuditDetailResponse, AuditHistoryItem
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audits", tags=["audits"])


@router.get("", response_model=list[AuditHistoryItem])
def list_audits(
    skip: int = 0,
    limit: int = 20,
    service: AuditService = Depends(get_audit_service),
):
    """Retorna a lista paginada de auditorias salvas."""
    return service.list_audits(skip=skip, limit=limit)


@router.get("/{audit_id}", response_model=AuditDetailResponse)
def get_audit(audit_id: int, service: AuditService = Depends(get_audit_service)):
    """Retorna os detalhes completos de uma auditoria."""
    try:
        return service.get_audit(audit_id)
    except AuditNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
