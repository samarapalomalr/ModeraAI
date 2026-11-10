from urllib.parse import urlparse

import requests

from app.core.exceptions import InvalidMediaURLError, MediaUnavailableError

# Apenas CDNs do Instagram/Meta (evita SSRF e uso como proxy aberto).
ALLOWED_HOST_SUFFIXES = ("cdninstagram.com", "fbcdn.net")
MAX_IMAGE_BYTES = 10 * 1024 * 1024


class MediaService:
    """Baixa a imagem do post no servidor, contornando o bloqueio de hotlink do CDN."""

    @staticmethod
    def _validate(url: str) -> None:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or not host.endswith(ALLOWED_HOST_SUFFIXES):
            print(f"[Media] host bloqueado pela allowlist: {host!r} (scheme={parsed.scheme})")
            raise InvalidMediaURLError("URL de imagem não permitida.")

    def fetch_image(self, url: str) -> tuple[bytes, str]:
        self._validate(url)
        try:
            res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
        except requests.RequestException as e:
            print(f"[Media] erro de rede ao baixar imagem: {e}")
            raise MediaUnavailableError(f"Falha ao baixar imagem: {e}")

        mime = res.headers.get("Content-Type", "").split(";")[0]
        if res.status_code != 200 or not mime.startswith("image/"):
            print(f"[Media] CDN respondeu status={res.status_code} content-type={mime!r} host={urlparse(url).hostname}")
            raise MediaUnavailableError("Imagem indisponível ou expirada.")
        if len(res.content) > MAX_IMAGE_BYTES:
            raise MediaUnavailableError("Imagem muito grande.")
        return res.content, mime
