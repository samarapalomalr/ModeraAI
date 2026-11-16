from typing import Any

from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.domain.interfaces.password_hasher import PasswordHasher
from app.domain.interfaces.token_service import TokenService
from app.domain.interfaces.user_repository import UserRepository

# Hash fictício usado para igualar o tempo de resposta quando o e-mail não existe.
_DUMMY_HASH = None


class AuthService:
    """Casos de uso: cadastro, login e identificação do usuário pelo token."""

    def __init__(self, users: UserRepository, hasher: PasswordHasher, tokens: TokenService):
        self._users = users
        self._hasher = hasher
        self._tokens = tokens

    def register(self, name: str, email: str, password: str) -> tuple[Any, str]:
        email = email.strip().lower()
        if self._users.get_by_email(email):
            raise EmailAlreadyRegisteredError("Este e-mail já está cadastrado.")
        user = self._users.add(name.strip(), email, self._hasher.hash(password))
        return user, self._tokens.create(user.id)

    def login(self, email: str, password: str) -> tuple[Any, str]:
        global _DUMMY_HASH
        user = self._users.get_by_email(email.strip().lower())
        if user is None:
            if _DUMMY_HASH is None:
                _DUMMY_HASH = self._hasher.hash("dummy-password")
            self._hasher.verify(password, _DUMMY_HASH)
            raise InvalidCredentialsError("E-mail ou senha incorretos.")
        if not self._hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError("E-mail ou senha incorretos.")
        return user, self._tokens.create(user.id)

    def get_current_user(self, token: str) -> Any:
        user = self._users.get_by_id(self._tokens.decode(token))
        if user is None:
            raise InvalidCredentialsError("Usuário não encontrado.")
        return user
