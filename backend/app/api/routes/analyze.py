from fastapi import APIRouter, HTTPException

from app.core.exceptions import InvalidPostURLError, PostDataNotFoundError
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services import analysis_service

router = APIRouter(tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_post(request: AnalyzeRequest):
    try:
        return analysis_service.analyze_post(request.post_url)
    except InvalidPostURLError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PostDataNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno na análise: {e}")
