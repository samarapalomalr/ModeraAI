import time

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.analyze_schema import AnalyzeRequest, AnalyzeResponse
from app.analyze_schema import AuditHistoryItem, AuditDetailResponse
from app.helpers import validate_instagram_url
from app.ai_service import analyze_post_with_ai
from app.instagram_service import fetch_instagram_data
from app.database import get_db
from app.models import Audit

router = APIRouter()

# -----------------------------
# CACHE EM MEMÓRIA
# Evita refazer Apify + Gemini para o mesmo link em poucos minutos
# (ótimo para demonstrações). Só guarda análises bem-sucedidas.
# -----------------------------
CACHE_TTL_SECONDS = 600  # 10 minutos
_cache: dict[str, tuple[float, dict]] = {}


def _cache_get(key: str):
    item = _cache.get(key)
    if not item:
        return None
    saved_at, value = item
    if time.time() - saved_at > CACHE_TTL_SECONDS:
        _cache.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: dict):
    _cache[key] = (time.time(), value)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_post(request: AnalyzeRequest):

    # -----------------------------
    # VALIDATE URL
    # -----------------------------
    if not validate_instagram_url(request.post_url):
        raise HTTPException(
            status_code=400,
            detail="URL inválida. Use um link do Instagram.",
        )

    cache_key = request.post_url.strip().rstrip("/")
    cached = _cache_get(cache_key)
    if cached:
        print(f"[Cache] resultado reaproveitado para {cache_key}")
        return cached

    try:
        t_start = time.time()

        # -----------------------------
        # SEARCH FOR INSTAGRAM DATA
        # -----------------------------
        post_data = fetch_instagram_data(request.post_url)
        t_apify = time.time()

        if not post_data:
            raise HTTPException(
                status_code=500,
                detail="Não foi possível obter dados do Instagram.",
            )

        # -----------------------------
        # ANALYZE WITH IA + BACKEND
        # -----------------------------
        result = analyze_post_with_ai(post_data)
        t_ai = time.time()

        print(
            f"[Tempo] Apify: {t_apify - t_start:.1f}s | "
            f"IA: {t_ai - t_apify:.1f}s | Total: {t_ai - t_start:.1f}s"
        )

        if not result.get("ai_failed"):
            _cache_set(cache_key, result)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na análise: {str(e)}",
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
