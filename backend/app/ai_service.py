import json
import re
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
# GEMINI CALL (MULTIMODAL)
# -----------------------------
def call_gemini(prompt: str, image_url: str = None) -> dict:
    try:
        contents = [prompt]
        
        if image_url:
            image_part = types.Part.from_uri(
                file_uri=image_url,
                mime_type="image/jpeg"
            )
            contents.append(image_part)

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents
        )

        text = extract_gemini_text(response)
        if not text:
            raise Exception("Resposta vazia do Gemini")

        cleaned = clean_json_text(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("[RAW GEMINI OUTPUT]:", text)
            raise Exception("Gemini não retornou JSON válido")

    except Exception as e:
        print(f"[Gemini error]: {e}")
        raise Exception(f"Falha no Gemini: {e}")

# -----------------------------
# ENGAGEMENT SCORE 
# -----------------------------
def calculate_engagement(likes: int, comments: int):

    total_interactions = (likes * 1) + (comments * 2.5) # Peso maior para comentários
    if total_interactions == 0: return 0
    
    # Simulação de taxa de engajamento (Normalizada para exibir no ResultCard)
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
    try:
        caption = clean_text(post_data.get("caption", ""))
        display_url = post_data.get("display_url")

        # Chama o extrator de precisão para garantir likes e comentários corretos
        likes, comments = get_precise_metrics(post_data)

        prompt = build_ai_prompt(post_data)
        prompt += "\nAnalise a imagem para validar se o conteúdo visual condiz com os números de engajamento."
        
        ai_result = call_gemini(prompt, image_url=display_url)

        engagement_score = calculate_engagement(likes, comments)
        virality = classify_virality(engagement_score)
        content_type = detect_content_type(caption, ai_result.get("content_type"))

        return {
            "metrics": {"likes": likes, "comments": comments},
            "display_url": display_url,
            "engagement_score": engagement_score,
            "viral_classification": virality,
            "content_type": content_type,
            "sentiment": ai_result.get("sentiment", "Neutro"),
            "insights": ai_result.get("insights", []),
            "recommendations": ai_result.get("recommendations", [])
        }

    except Exception as error:
        print(f"[AI ERROR]: {error}")
        l, c = get_precise_metrics(post_data)
        return {
            "metrics": {"likes": l, "comments": c},
            "engagement_score": 0,
            "viral_classification": "Análise Pendente",
            "content_type": "Geral",
            "sentiment": "Neutro",
            "insights": ["Erro técnico ao processar metadados detalhados."],
            "recommendations": ["Tente atualizar o link do post."]
        }