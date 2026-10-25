import requests
from app.config import settings

# Endpoint do Apify Instagram Scraper
APIFY_URL = "https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items"

def fetch_instagram_data(url: str):
    """
    Busca dados do Instagram via Apify.
    Agora captura a imagem de exibição para análise multimodal da IA.
    """

    if not settings.APIFY_API_KEY:
        raise Exception("APIFY_API_KEY não configurada no .env")

    # Payload optimized for specific posts
    payload = {
        "directUrls": [url],
        "resultsType": "posts",
        "resultsLimit": 1
    }

    try:
        response = requests.post(
            f"{APIFY_URL}?token={settings.APIFY_API_KEY}",
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        if not data or len(data) == 0:
            return {
                "caption": "",
                "likes": 0,
                "comments": 0,
                "hashtags": [],
                "display_url": None
            }

        post = data[0]

        return {
            "caption": post.get("caption", "") or "",
            "likes": int(post.get("likesCount", 0) or 0),
            "comments": int(post.get("commentsCount", 0) or 0),
            "hashtags": post.get("hashtags", []) or [],
            "display_url": post.get("displayUrl")
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao acessar Apify: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro ao processar dados do Instagram: {str(e)}")