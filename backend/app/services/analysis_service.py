import json
import time
from typing import Optional

from app.core.exceptions import InvalidPostURLError, PostDataUnavailableError
from app.domain.interfaces.audit_repository import AuditRepository
from app.domain.interfaces.content_analyzer import ContentAnalyzer
from app.domain.interfaces.post_scraper import PostScraper
from app.domain.interfaces.result_cache import ResultCache
from app.utils.helpers import validate_instagram_url


class AnalysisService:
    """Caso de uso: validar URL -> cache -> coletar post -> analisar com IA -> persistir auditoria.

    Depende apenas de abstrações (DIP) injetadas pelo construtor.
    """

    def __init__(
        self,
        scraper: PostScraper,
        analyzer: ContentAnalyzer,
        cache: ResultCache,
        audit_repository: Optional[AuditRepository] = None,
    ):
        self._scraper = scraper
        self._analyzer = analyzer
        self._cache = cache
        self._audit_repo = audit_repository

    def analyze_post(self, post_url: str, platform: str = "instagram") -> dict:
        if not validate_instagram_url(post_url):
            raise InvalidPostURLError("URL inválida. Use um link do Instagram.")

        cache_key = post_url.strip().rstrip("/")
        cached = self._cache.get(cache_key)
        if cached:
            print(f"[Cache] resultado reaproveitado para {cache_key}")
            return cached

        t_start = time.time()
        post_data = self._scraper.fetch_post(post_url)
        t_scrape = time.time()

        if not post_data:
            raise PostDataUnavailableError("Não foi possível obter dados do Instagram.")

        result = self._analyzer.analyze(post_data)
        t_ai = time.time()

        print(
            f"[Tempo] Apify: {t_scrape - t_start:.1f}s | "
            f"IA: {t_ai - t_scrape:.1f}s | Total: {t_ai - t_start:.1f}s"
        )

        if not result.get("ai_failed"):
            self._cache.set(cache_key, result)

        # Persistência no banco de dados (atendendo ao fluxo 6 da proposta)
        if self._audit_repo:
            try:
                # O compliance_score pode ser o inverso da toxicidade (ex: 100 - toxicidade)
                toxicity = result.get("toxicity_score")
                compliance_score = int(max(0, 100 - toxicity)) if toxicity is not None else None
                
                self._audit_repo.save(
                    platform=platform,
                    target_url=post_url,
                    raw_content=post_data.get("caption", ""),
                    summary=result.get("summary", ""),
                    compliance_score=compliance_score,
                    result_json=json.dumps(result, ensure_ascii=False),
                    status="FAILED" if result.get("ai_failed") else "COMPLETED",
                )
            except Exception as e:
                print(f"[Audit] Aviso: falha ao salvar auditoria no histórico: {e}")

        return result
