from abc import ABC, abstractmethod
from typing import Optional


class ResultCache(ABC):
    """Contrato de cache de resultados de análise."""

    @abstractmethod
    def get(self, key: str) -> Optional[dict]: ...

    @abstractmethod
    def set(self, key: str, value: dict) -> None: ...
