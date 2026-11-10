import requests

from app.domain.interfaces.post_scraper import PostScraper

# Endpoint do Apify Instagram Scraper
APIFY_URL = "https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items"

MAX_COMMENTS_FOR_AI = 30


def _safe_int(value) -> int:
    """Converte para int. O Apify devolve -1 quando o dado está oculto; tratamos como 0."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _extract_top_comments(post: dict) -> list[dict]:
    """
    Pega os comentários que o Apify devolve em 'latestComments' e ordena
    pelos mais curtidos. Mantém só o necessário para a análise da IA.
    """
    raw = post.get("latestComments") or []
    if not isinstance(raw, list):
        return []

    comments = []
    for c in raw:
        if not isinstance(c, dict):
            continue
        text = (c.get("text") or "").strip()
        if not text:
            continue
        comments.append(
            {
                "text": text,
                "owner": c.get("ownerUsername") or "",
                "likes": _safe_int(c.get("likesCount")),
            }
        )

    comments.sort(key=lambda c: c["likes"], reverse=True)
    return comments[:MAX_COMMENTS_FOR_AI]


class ApifyPostScraper(PostScraper):
    """Coleta dados de posts do Instagram via Apify."""

    def __init__(self, api_key: str | None):
        self._api_key = api_key

    def fetch_post(self, url: str) -> dict:
        """
        Busca dados do Instagram via Apify.
        Captura a imagem de exibição e os comentários para a análise multimodal da IA.
        """

        if not self._api_key:
            raise Exception("APIFY_API_KEY não configurada no .env")

        # Payload otimizado para um post específico
        payload = {
            "directUrls": [url],
            "resultsType": "posts",
            "resultsLimit": 1,
        }

        try:
            response = requests.post(
                f"{APIFY_URL}?token={self._api_key}",
                json=payload,
                timeout=60,
            )

            response.raise_for_status()
            data = response.json()

            if not data or len(data) == 0:
                return {
                    "caption": "",
                    "likes": 0,
                    "comments": 0,
                    "hashtags": [],
                    "display_url": None,
                    "top_comments": [],
                }

            post = data[0]

            return {
                "caption": post.get("caption", "") or "",
                "likes": _safe_int(post.get("likesCount")),
                "comments": _safe_int(post.get("commentsCount")),
                "hashtags": post.get("hashtags", []) or [],
                "display_url": post.get("displayUrl") or (post.get("images") or [None])[0],
                # Novos campos usados pela IA para inferir o contexto do post
                "top_comments": _extract_top_comments(post),
                "owner": post.get("ownerUsername") or post.get("ownerFullName") or "",
                "type": post.get("type") or post.get("productType") or "",
                "alt": post.get("alt") or "",
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao acessar Apify: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar dados do Instagram: {str(e)}")
