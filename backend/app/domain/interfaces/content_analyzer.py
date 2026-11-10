from abc import ABC, abstractmethod
from typing import Any


class ContentAnalyzer(ABC):
    """Contrato para análise de conteúdo por IA."""

    @abstractmethod
    def analyze(self, post: dict[str, Any]) -> dict[str, Any]: ...
