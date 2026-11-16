"""Regras de negócio puras de pontuação (sem I/O)."""
from app.utils.helpers import to_int

def get_precise_metrics(post_data: dict):
    likes = to_int(post_data.get("likes", 0))
    comments = to_int(post_data.get("comments", 0))

    comments_count = post_data.get("commentsCount") or post_data.get(
        "edge_media_to_parent_comment", {}
    ).get("count")
    if comments_count and to_int(comments_count) > comments:
        comments = to_int(comments_count)

    return likes, comments


def calculate_engagement(likes: int, comments: int):
    total_interactions = (likes * 1) + (comments * 2.5)
    if total_interactions == 0:
        return 0
    return round(total_interactions / 100, 2)


# -----------------------------
# VIRAL CLASSIFICATION
# -----------------------------
def classify_virality(score: float) -> str:
    if score >= 100:
        return "Explosivo"
    elif score >= 50:
        return "Viral"
    elif score >= 15:
        return "Alto"
    return "Estável"


# -----------------------------
# CONTENT TYPE DETECTION
# -----------------------------
def detect_content_type(text: str, ai_suggestion: str = None) -> str:
    if ai_suggestion and ai_suggestion.lower() != "geral":
        return ai_suggestion

    text = (text or "").lower()
    if any(w in text for w in ["😂", "🤣", "meme", "humor"]):
        return "Humor"
    if any(w in text for w in ["dica", "tutorial", "como"]):
        return "Educativo"
    return "Lifestyle"
