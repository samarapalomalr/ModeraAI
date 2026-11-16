from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.analyze import (
    AnalyzeRequest,
    AnalyzeResponse,
    AuditDetailResponse,
    AuditHistoryItem,
)
from app.core.dependencies import get_analysis_service, get_audit_service
from app.core.exceptions import (
    AuditNotFoundError,
    InvalidPostURLError,
    PostDataUnavailableError,
)
from app.services.analysis_service import AnalysisService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_post(request: AnalyzeRequest, service: AnalysisService = Depends(get_analysis_service)):
    try:
        return service.analyze_post(request.post_url)
    except InvalidPostURLError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PostDataUnavailableError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno na análise: {str(e)}")


@router.get("/audits", response_model=list[AuditHistoryItem])
def list_audits(skip: int = 0, limit: int = 20, service: AuditService = Depends(get_audit_service)):
    """Retorna a lista paginada de auditorias salvas."""
    return service.list_audits(skip, limit)


@router.get("/audits/{audit_id}", response_model=AuditDetailResponse)
def get_audit(audit_id: int, service: AuditService = Depends(get_audit_service)):
    """Retorna os detalhes completos de uma auditoria."""
    try:
        return service.get_audit(audit_id)
    except AuditNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
