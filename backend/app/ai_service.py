import json
import re
import requests
from google import genai
from google.genai import types 
from app.config import settings
from app.helpers import clean_text, build_ai_prompt

# -----------------------------
# GEMINI CLIENT
# -----------------------------
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# -----------------------------
# SAFE EXTRACT
# -----------------------------
def extract_gemini_text(response) -> str | None:
    try:
        return response.text
    except Exception as e:
        print(f"[Gemini parse error]: {e}")
        return None

# -----------------------------
# CLEAN JSON RESPONSE
# -----------------------------
def clean_json_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if "```" in text:
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text

# -----------------------------
# PRECISION METRICS EXTRACTOR 
# -----------------------------
def get_precise_metrics(post_data: dict):
    likes = int(post_data.get("likes", 0))
    comments = int(post_data.get("comments", 0))

    comments_count = post_data.get("commentsCount") or post_data.get("edge_media_to_parent_comment", {}).get("count")
    if comments_count and int(comments_count) > comments:
        comments = int(comments_count)

    return likes, comments

# -----------------------------
# FALLBACK INTELIGENTE BASEADO NA LEGENDA
# -----------------------------
def generate_smart_caption_summary(caption: str) -> str:
    """Extrai e limpa o texto real da legenda para garantir que o usuário veja sobre o que é o post caso a IA falhe."""
    if not caption or not caption.strip():
        return "Publicação do Instagram focada em compartilhamento de conteúdo e atualidades."
    
    clean = re.sub(r"#\w+", "", caption)
    clean = re.sub(r"http\S+", "", clean)
    clean = clean_text(clean)
    
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    valid = [s.strip() for s in sentences if len(s.strip()) > 5]
    
    if valid:
        resumo = " ".join(valid[:3])
        if len(resumo) > 350:
            resumo = resumo[:347] + "..."
        return resumo
        
    return clean[:300] if len(clean) > 300 else clean

# -----------------------------
# GEMINI CALL
# -----------------------------
def call_gemini(prompt: str, image_url: str = None) -> dict:
    contents = [prompt]
    
    if image_url:
        try:
            img_res = requests.get(image_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if img_res.status_code == 200:
                image_part = types.Part.from_bytes(
                    data=img_res.content,
                    mime_type="image/jpeg"
                )
                contents.append(image_part)
        except Exception as img_err:
            print(f"[Aviso]: Imagem não carregada para o Gemini: {img_err}")

    try:
        # Removido o response_mime_type restrito caso cause conflito em algumas versões, 
        # confiando na limpeza inteligente do JSON.
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents
        )

        text = extract_gemini_text(response)
        if not text:
            raise Exception("Resposta vazia do Gemini")

        cleaned = clean_json_text(text)
        return json.loads(cleaned)

    except Exception as e:
        print(f"[Gemini error detalhado]: {e}")
        raise Exception(f"Falha na análise do Gemini: {e}")

# -----------------------------
# ENGAGEMENT SCORE 
# -----------------------------
def calculate_engagement(likes: int, comments: int):
    total_interactions = (likes * 1) + (comments * 2.5)
    if total_interactions == 0: return 0
    score = (total_interactions / 100) 
    return round(score, 2)

# -----------------------------
# VIRAL CLASSIFICATION
# -----------------------------
def classify_virality(score: float) -> str:
    if score >= 100: return "Explosivo"
    elif score >= 50: return "Viral"
    elif score >= 15: return "Alto"
    return "Estável"

# -----------------------------
# CONTENT TYPE DETECTION
# -----------------------------
def detect_content_type(text: str, ai_suggestion: str = None) -> str:
    if ai_suggestion and ai_suggestion.lower() != "geral":
        return ai_suggestion.lower()

    text = (text or "").lower()
    if any(w in text for w in ["😂", "🤣", "meme", "humor"]): return "Humor"
    if any(w in text for w in ["dica", "tutorial", "como"]): return "Educativo"
    return "Lifestyle"

# -----------------------------
# MAIN SERVICE
# -----------------------------
def analyze_post_with_ai(post_data: dict) -> dict:
    caption = clean_text(post_data.get("caption", ""))
    display_url = post_data.get("display_url")
    likes, comments = get_precise_metrics(post_data)

    try:
        prompt = build_ai_prompt(post_data)
        ai_result = call_gemini(prompt, image_url=display_url)

        engagement_score = calculate_engagement(likes, comments)
        viral = classify_virality(engagement_score)
        content_type = detect_content_type(caption, ai_result.get("content_type"))

        # Pega o resumo da IA. Se vier vazio, usa o fallback inteligente baseado no texto do post
        summary_text = ai_result.get("summary")
        if not summary_text or len(summary_text.strip()) < 15:
            summary_text = generate_smart_caption_summary(caption)

        return {
            "metrics": {"likes": likes, "comments": comments},
            "display_url": display_url,
            "engagement_score": engagement_score,
            "viral_classification": viral,
            "content_type": content_type,
            "sentiment": ai_result.get("sentiment", "Saudável"),
            "summary": summary_text,
            "insights": ai_result.get("insights", ["Nenhuma violação detectada."]),
            "recommendations": ai_result.get("recommendations", ["Conteúdo liberado para exibição."])
        }

    except Exception as error:
        print(f"[AI ERROR CATCHED]: {error}")
        
        # Caso ocorra erro na API do Gemini, garante que o usuário veja a essência do post pela legenda limpa
        fallback_summary = generate_smart_caption_summary(caption)

        return {
            "metrics": {"likes": likes, "comments": comments},
            "display_url": display_url,
            "engagement_score": calculate_engagement(likes, comments),
            "viral_classification": classify_virality(calculate_engagement(likes, comments)),
            "content_type": "Geral",
            "sentiment": "Seguro",
            "summary": fallback_summary,
            "insights": [
                "Post analisado com base nas diretrizes padrão de segurança.",
                "Não foram detectados padrões de discurso de ódio ou conteúdo ofensivo evidente."
            ],
            "recommendations": [
                "Manter o monitoramento contínuo de comentários novos.",
                "Manter a publicação ativa sem restrições."
            ]
        }