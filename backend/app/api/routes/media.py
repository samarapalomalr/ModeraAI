from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.dependencies import get_media_service
from app.core.exceptions import InvalidMediaURLError, MediaUnavailableError
from app.services.media_service import MediaService

router = APIRouter()


@router.get("/media")
def get_media(url: str, service: MediaService = Depends(get_media_service)):
    """Proxy da imagem do post (o CDN do Instagram bloqueia hotlink no navegador)."""
    try:
        content, mime = service.fetch_image(url)
    except InvalidMediaURLError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except MediaUnavailableError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return Response(content=content, media_type=mime, headers={"Cache-Control": "public, max-age=3600"})
