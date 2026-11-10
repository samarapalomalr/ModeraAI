"""Normalização e validação dos campos retornados pela IA (sem I/O)."""
import re
from difflib import SequenceMatcher

VALID_AGE_RATINGS = ["Livre", "10+", "12+", "14+", "16+", "18+"]


def normalize_age_rating(value) -> str:
    """Garante que a faixa etária seja um dos valores válidos."""
    text = str(value or "").strip().lower()
    if text in ("livre", "l", "todos", "0+"):
        return "Livre"
    match = re.search(r"\d+", text)
    if match:
        n = int(match.group(0))
        for rating, limit in (("10+", 10), ("12+", 12), ("14+", 14), ("16+", 16), ("18+", 18)):
            if n <= limit:
                return rating
        return "18+"
    return "Indeterminado"


# -----------------------------
# TOXICIDADE E RISCO
# -----------------------------
VALID_HARM = {"sem risco": "Sem Risco", "baixo": "Baixo", "moderado": "Moderado", "alto": "Alto", "crítico": "Crítico", "critico": "Crítico"}


def normalize_toxicity(value):
    """Número entre 0 e 100 (arredondado), ou None se inválido."""
    try:
        n = float(str(value).replace("%", "").replace(",", ".").strip())
    except (TypeError, ValueError):
        return None
    return round(min(max(n, 0.0), 100.0), 2)


def normalize_harm(value) -> str:
    return VALID_HARM.get(str(value or "").strip().lower(), "Indeterminado")


# -----------------------------
# DETECÇÃO DE CÓPIA DA LEGENDA
# -----------------------------
def _normalize(text: str) -> str:
    text = re.sub(r"#\w+|http\S+", "", text or "")
    text = re.sub(r"[^\w\s]", "", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def is_copy_of_caption(summary: str, caption: str) -> bool:
    """True se o resumo é praticamente a legenda (cópia ou paráfrase muito próxima)."""
    s, c = _normalize(summary), _normalize(caption)
    if not s or not c:
        return False
    if c in s or s in c:
        return True
    return SequenceMatcher(None, s, c).ratio() > 0.75
