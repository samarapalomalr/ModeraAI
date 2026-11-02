from fastapi import APIRouter, HTTPException, Depends

from app.analyze_schema import AnalyzeRequest, AnalyzeResponse
from app.helpers import validate_instagram_url
from app.ai_service import analyze_post_with_ai
from app.instagram_service import fetch_instagram_data
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Audit
from app.analyze_schema import AuditHistoryItem, AuditDetailResponse
import json


router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_post(request: AnalyzeRequest):

    # -----------------------------
    # VALIDATE URL
    # -----------------------------
    if not validate_instagram_url(request.post_url):
        raise HTTPException(
            status_code=400,
            detail="URL inválida. Use um link do Instagram."
        )

    try:
        # -----------------------------
        # SEARCH FOR INSTAGRAM DATA
        # -----------------------------
        post_data = fetch_instagram_data(request.post_url)

        if not post_data:
            raise HTTPException(
                status_code=500,
                detail="Não foi possível obter dados do Instagram."
            )

        # -----------------------------
        # ANALYZE WITH IA + BACKEND
        # -----------------------------
        result = analyze_post_with_ai(post_data)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na análise: {str(e)}"
        )

# Endpoints de historico exigidos pela Issue #12:
@router.get("/audits", response_model=list[AuditHistoryItem])
def list_audits(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Retorna a lista paginada de auditorias salvas."""
    return db.query(Audit).order_by(Audit.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/audits/{audit_id}", response_model=AuditDetailResponse)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes completos de uma auditoria."""
    record = db.query(Audit).filter(Audit.id == audit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Auditoria não encontrada")
    return record
