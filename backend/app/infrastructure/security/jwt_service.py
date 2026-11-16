from datetime import datetime, timedelta, timezone

import jwt

from app.core.exceptions import InvalidTokenError
from app.domain.interfaces.token_service import TokenService


class JwtTokenService(TokenService):
    def __init__(self, secret: str, expire_minutes: int):
        self._secret = secret
        self._expire = timedelta(minutes=expire_minutes)

    def create(self, user_id: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {"sub": str(user_id), "iat": now, "exp": now + self._expire}
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def decode(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self._secret, algorithms=["HS256"])
            return int(payload["sub"])
        except (jwt.PyJWTError, KeyError, ValueError):
            raise InvalidTokenError("Token inválido ou expirado.")
