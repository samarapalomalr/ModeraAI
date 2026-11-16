from app.domain.interfaces.content_analyzer import ContentAnalyzer
from app.domain.normalizers import (
    is_copy_of_caption,
    normalize_age_rating,
    normalize_harm,
    normalize_toxicity,
)
from app.domain.scoring import (
    calculate_engagement,
    classify_virality,
    detect_content_type,
    get_precise_metrics,
)
from app.infrastructure.ai.gemini_client import GeminiClient
from app.infrastructure.ai.prompt_builder import build_inference_prompt, extract_comment_texts
from app.utils.helpers import clean_text

SUMMARY_FAILED_MSG = "Não foi possível gerar o resumo automático desta publicação."


class GeminiContentAnalyzer(ContentAnalyzer):
    """Orquestra prompt + Gemini + regras de domínio para produzir a análise."""

    def __init__(self, client: GeminiClient):
        self._client = client

    def _generate_inferred_analysis(self, post_data: dict, caption: str) -> dict:
        """Chama o Gemini até 2 vezes; na 2ª o prompt fica mais rígido se o resumo copiou a legenda."""
        comments = extract_comment_texts(post_data)
        display_url = post_data.get("display_url")

        result = None
        for attempt in range(2):
            prompt = build_inference_prompt(post_data, caption, comments, strict=(attempt == 1))
            result = self._client.generate_json(prompt, image_url=display_url)

            summary = (result.get("summary") or "").strip()
            if len(summary) >= 15 and not is_copy_of_caption(summary, caption):
                return result
            print(f"[Resumo] tentativa {attempt + 1} copiou a legenda ou veio vazio; retentando...")

        return result  # devolve o último resultado mesmo assim

    def analyze(self, post: dict) -> dict:
        caption = clean_text(post.get("caption", ""))
        display_url = post.get("display_url")
        likes, comments = get_precise_metrics(post)
        engagement_score = calculate_engagement(likes, comments)
        viral = classify_virality(engagement_score)

        try:
            ai_result = self._generate_inferred_analysis(post, caption)

            summary_text = (ai_result.get("summary") or "").strip()
            if len(summary_text) < 15:
                summary_text = SUMMARY_FAILED_MSG

            return {
                "metrics": {"likes": likes, "comments": comments},
                "display_url": display_url,
                "engagement_score": engagement_score,
                "viral_classification": viral,
                "content_type": detect_content_type(caption, ai_result.get("content_type")),
                "sentiment": ai_result.get("sentiment", "Saudável"),
                "age_rating": normalize_age_rating(ai_result.get("age_rating")),
                "toxicity_score": normalize_toxicity(ai_result.get("toxicity_score")),
                "harm_classification": normalize_harm(ai_result.get("harm_classification")),
                "summary": summary_text,
                "insights": ai_result.get("insights") or ["Nenhuma violação detectada."],
                "recommendations": ai_result.get("recommendations") or ["Conteúdo liberado para exibição."],
                "ai_failed": False,
            }

        except Exception as error:
            print(f"[AI ERROR CATCHED]: {error}")

            # Fallback honesto: NÃO copia a legenda e NÃO afirma que o post é seguro.
            return {
                "metrics": {"likes": likes, "comments": comments},
                "display_url": display_url,
                "engagement_score": engagement_score,
                "viral_classification": viral,
                "content_type": "Geral",
                "sentiment": "Indeterminado",
                "age_rating": "Indeterminado",
                "toxicity_score": None,
                "harm_classification": "Indeterminado",
                "summary": SUMMARY_FAILED_MSG,
                "insights": [
                    "A análise por IA não pôde ser concluída para este post.",
                    "Revise o conteúdo manualmente ou tente analisar novamente.",
                ],
                "recommendations": [
                    "Tentar a análise novamente em alguns instantes.",
                    "Fazer revisão manual enquanto a análise automática estiver indisponível.",
                ],
                "ai_failed": True,
            }
