"""Orquestra o fluxo: validar URL -> coletar (Apify) -> analisar (Gemini)."""
from app.core.exceptions import InvalidPostURLError, PostDataNotFoundError
from app.services.ai_service import analyze_post_with_ai
from app.services.instagram_service import fetch_instagram_data
from app.utils.validators import validate_instagram_url


def analyze_post(post_url: str) -> dict:
    if not validate_instagram_url(post_url):
        raise InvalidPostURLError("URL inválida. Use um link do Instagram.")

    post_data = fetch_instagram_data(post_url)
    if not post_data:
        raise PostDataNotFoundError("Não foi possível obter dados do Instagram.")

    return analyze_post_with_ai(post_data)
