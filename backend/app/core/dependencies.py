"""Composition root: único lugar que conhece as implementações concretas."""
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.ai.gemini_analyzer import GeminiContentAnalyzer
from app.infrastructure.ai.gemini_client import GeminiClient
from app.infrastructure.cache.memory_cache import InMemoryResultCache
from app.infrastructure.database.session import get_db
from app.infrastructure.scraping.apify_scraper import ApifyPostScraper
from app.repositories.audit_repository import SqlAlchemyAuditRepository
from app.infrastructure.security.jwt_service import JwtTokenService
from app.infrastructure.security.scrypt_hasher import ScryptPasswordHasher
from app.repositories.user_repository import SqlAlchemyUserRepository
from app.services.analysis_service import AnalysisService
from app.services.audit_service import AuditService
from app.services.auth_service import AuthService
from app.services.media_service import MediaService


@lru_cache
def _result_cache() -> InMemoryResultCache:
    # Singleton: o cache precisa sobreviver entre requisições.
    return InMemoryResultCache(ttl_seconds=600)


@lru_cache
def _analyzer() -> GeminiContentAnalyzer:
    return GeminiContentAnalyzer(GeminiClient(settings.GEMINI_API_KEY, settings.GEMINI_MODEL))


def get_analysis_service(db: Session = Depends(get_db)) -> AnalysisService:
    return AnalysisService(
        ApifyPostScraper(settings.APIFY_API_KEY),
        _analyzer(),
        _result_cache(),
        SqlAlchemyAuditRepository(db),
    )


def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(SqlAlchemyAuditRepository(db))


def get_media_service() -> MediaService:
    return MediaService()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        SqlAlchemyUserRepository(db),
        ScryptPasswordHasher(),
        JwtTokenService(settings.JWT_SECRET, settings.JWT_EXPIRE_MINUTES),
    )
