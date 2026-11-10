from abc import ABC, abstractmethod
from typing import Any, Optional


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Any]: ...

    @abstractmethod
    def add(self, name: str, email: str, password_hash: str) -> Any: ...
