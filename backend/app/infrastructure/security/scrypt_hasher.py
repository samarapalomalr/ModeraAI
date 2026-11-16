import base64
import hashlib
import hmac
import os

from app.domain.interfaces.password_hasher import PasswordHasher

# Parâmetros do scrypt (stdlib, sem dependências extras).
_N, _R, _P = 2**14, 8, 1


class ScryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P)
        return "scrypt${}${}".format(base64.b64encode(salt).decode(), base64.b64encode(digest).decode())

    def verify(self, password: str, hashed: str) -> bool:
        try:
            _, salt_b64, digest_b64 = hashed.split("$")
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(digest_b64)
        except ValueError:
            return False
        digest = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P)
        return hmac.compare_digest(digest, expected)
