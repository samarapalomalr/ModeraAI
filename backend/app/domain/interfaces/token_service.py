from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def create(self, user_id: int) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> int:
        """Retorna o id do usuário ou levanta InvalidTokenError."""
