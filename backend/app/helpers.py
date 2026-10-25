import re
from urllib.parse import urlparse


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def extract_hashtags(text: str):
    return re.findall(r"#\w+", text or "")


def validate_instagram_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return "instagram.com" in parsed.netloc
    except Exception:
        return False


def build_ai_prompt(post_data: dict) -> str:
    return f"""
Você é um analista profissional de redes sociais especializado em Instagram.

Sua tarefa é analisar o conteúdo de um post e gerar insights estratégicos.

🚨 REGRAS OBRIGATÓRIAS:
- Responda SOMENTE com JSON válido
- NÃO use markdown
- NÃO explique nada fora do JSON
- NÃO invente dados numéricos

⚠️ IMPORTANTE:
- NÃO retorne métricas (likes, comentários, seguidores)
- NÃO calcule engajamento
- NÃO classifique viralidade
- NÃO defina tipo de conteúdo

👉 Foque APENAS em:
- sentiment (positivo, neutro ou negativo)
- insights estratégicos
- recomendações acionáveis

📦 FORMATO OBRIGATÓRIO:

{{
  "sentiment": "positivo | neutro | negativo",
  "insights": [
    "insight 1",
    "insight 2"
  ],
  "recommendations": [
    "recomendação 1",
    "recomendação 2"
  ]
}}

📌 DADOS DO POST:
Legenda: {post_data.get("caption", "")}
Hashtags: {", ".join(post_data.get("hashtags", []))}
"""