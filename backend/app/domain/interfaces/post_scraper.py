from abc import ABC, abstractmethod
from typing import Any


class PostScraper(ABC):
    """Contrato para coleta de dados de uma publicação (ISP/DIP)."""

    @abstractmethod
    def fetch_post(self, url: str) -> dict[str, Any]: ...
