from urllib.parse import urlparse


def validate_instagram_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return "instagram.com" in parsed.netloc
    except Exception:
        return False
