import json
import re
import time
from difflib import SequenceMatcher

import requests
from google import genai
from google.genai import types

from app.config import settings
from app.helpers import clean_text

# -----------------------------
# GEMINI CLIENT
# -----------------------------
client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=30000),  # 30 s
)

# Modelos tentados em ordem: o do .env primeiro, depois alternativas
# (usadas quando o principal responde 503/429 por alta demanda).
FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]
RETRY_SAME_MODEL = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")  # sobrecarga: espera e repete

SUMMARY_FAILED_MSG = "Não foi possível gerar o resumo automático desta publicação."


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
# HELPERS DE DADOS
# -----------------------------
def _to_int(value) -> int:
    """Converte para int de forma segura (aceita número, string ou lista)."""
    if isinstance(value, (list, tuple)):
        return len(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def get_precise_metrics(post_data: dict):
    likes = _to_int(post_data.get("likes", 0))
    comments = _to_int(post_data.get("comments", 0))

    comments_count = post_data.get("commentsCount") or post_data.get(
        "edge_media_to_parent_comment", {}
    ).get("count")
    if comments_count and _to_int(comments_count) > comments:
        comments = _to_int(comments_count)

    return likes, comments


def extract_comment_texts(post_data: dict, limit: int = 30) -> list[str]:
    """
    Extrai o texto dos comentários, se o instagram_service os repassar.
    Tenta várias chaves possíveis (ajuste conforme o que seu post_data tiver).
    """
    raw = (
        post_data.get("top_comments")
        or post_data.get("latestComments")
        or post_data.get("comments_list")
        or post_data.get("comments_data")
        or []
    )
    if not isinstance(raw, list):
        return []

    texts = []
    for item in raw:
        if isinstance(item, dict):
            text = item.get("text") or item.get("comment") or ""
        else:
            text = str(item)
        text = clean_text(text or "")
        if text and len(text) > 2:
            texts.append(text[:200])
        if len(texts) >= limit:
            break
    return texts


# -----------------------------
# PROMPT (INFERÊNCIA AUTÔNOMA)
# -----------------------------
def build_inference_prompt(post_data: dict, caption: str, comments: list[str], strict: bool = False) -> str:
    hashtags = re.findall(r"#\w+", caption or "")
    owner = post_data.get("owner") or post_data.get("ownerUsername") or "não informado"
    post_type = post_data.get("type") or post_data.get("product_type") or "não informado"
    alt_text = post_data.get("alt") or ""

    comments_block = "\n".join(f"- {c}" for c in comments) if comments else "(sem comentários disponíveis)"
    total_comments = _to_int(post_data.get("comments", 0))

    extra_rule = ""
    if strict:
        extra_rule = (
            "\nATENÇÃO: sua resposta anterior repetiu a legenda. "
            "Agora escreva o resumo com palavras totalmente diferentes, "
            "descrevendo o que o post É, e não o que ele diz.\n"
        )

    return f"""Você é um analista sênior de moderação de conteúdo e mídias sociais.
Analise a publicação do Instagram abaixo usando TODAS as fontes disponíveis:
a imagem anexada (se houver), a legenda, as hashtags, os comentários e os metadados.

DADOS DA PUBLICAÇÃO
- Perfil: {owner}
- Tipo de mídia: {post_type}
- Texto alternativo da imagem: {alt_text or "(não disponível)"}
- Hashtags: {", ".join(hashtags) if hashtags else "(nenhuma)"}
- Legenda: {caption or "(sem legenda)"}
- Total de comentários no post: {total_comments} (abaixo, apenas uma amostra dos mais curtidos)
- Comentários em destaque:
{comments_block}

REGRAS PARA O CAMPO "summary" (as mais importantes):
1. Escreva de 2 a 3 frases completas, em português, em terceira pessoa.
2. É uma INFERÊNCIA SUA, não uma cópia: NUNCA repita nem parafraseie de perto a legenda.
3. Diga qual é o tema, o formato (ex.: trecho de podcast, meme, tutorial, anúncio),
   o tom e o público provável, e como a audiência está reagindo (com base nos comentários).
4. Se a legenda for só uma chamada ("link na bio", "novo episódio"), deduza o contexto
   pela imagem, hashtags, perfil e comentários.
5. Se não houver informação suficiente, diga isso de forma honesta em vez de inventar.
6. Termine sempre a frase com ponto final. Não use reticências.

REGRAS PARA "toxicity_score" e "harm_classification":
- "toxicity_score": número de 0 a 100 estimando quanto do conteúdo analisado (legenda, imagem e comentários)
  é tóxico (ofensas, ódio, assédio, ameaças, desinformação nociva). 0 = nada tóxico.
  Seja calibrado: tema polêmico mas debatido com respeito deve ficar baixo. Nunca passe de 100.
- "harm_classification": nível de risco para moderação: "Sem Risco", "Baixo", "Moderado", "Alto" ou "Crítico".

REGRAS PARA O CAMPO "age_rating" (classificação indicativa brasileira):
Escolha exatamente um valor entre: "Livre", "10+", "12+", "14+", "16+", "18+".
Considere linguagem, violência, sexualidade, drogas, temas sensíveis e a imagem.
Na dúvida entre duas faixas, escolha a mais restritiva.
{extra_rule}
Responda APENAS com um JSON válido, sem markdown, neste formato exato:
{{
  "content_type": "Humor | Educativo | Lifestyle | Notícia | Publicidade | Entretenimento | Outro",
  "sentiment": "Saudável | Neutro | Polêmico | Tóxico",
  "age_rating": "Livre | 10+ | 12+ | 14+ | 16+ | 18+",
  "toxicity_score": 0,
  "harm_classification": "Sem Risco | Baixo | Moderado | Alto | Crítico",
  "summary": "resumo inferencial seguindo as regras acima",
  "insights": ["2 a 4 observações objetivas sobre riscos, tom dos comentários e conformidade"],
  "recommendations": ["2 a 3 ações práticas de moderação"]
}}"""


# -----------------------------
# FAIXA ETÁRIA
# -----------------------------
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


# -----------------------------
# GEMINI CALL
# -----------------------------
def call_gemini(prompt: str, image_url: str = None) -> dict:
    contents = [prompt]

    if image_url:
        try:
            img_res = requests.get(image_url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
            if img_res.status_code == 200:
                mime = img_res.headers.get("Content-Type", "image/jpeg").split(";")[0]
                if not mime.startswith("image/"):
                    mime = "image/jpeg"
                contents.append(types.Part.from_bytes(data=img_res.content, mime_type=mime))
        except Exception as img_err:
            print(f"[Aviso]: Imagem não carregada para o Gemini: {img_err}")

    # Em moderação o modelo precisa poder LER conteúdo ofensivo sem ser bloqueado.
    safety = [
        types.SafetySetting(category=cat, threshold="BLOCK_NONE")
        for cat in (
            "HARM_CATEGORY_HARASSMENT",
            "HARM_CATEGORY_HATE_SPEECH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "HARM_CATEGORY_DANGEROUS_CONTENT",
        )
    ]

    def build_config(model_name: str) -> types.GenerateContentConfig:
        # Gemini 3.x controla o raciocínio por "thinking_level"; o 2.5 usa "thinking_budget".
        if model_name.startswith("gemini-2.5"):
            thinking = types.ThinkingConfig(thinking_budget=0)
        else:
            thinking = types.ThinkingConfig(thinking_level="low")
        return types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=2048,
            thinking_config=thinking,
            safety_settings=safety,
        )

    models = [settings.GEMINI_MODEL] + [m for m in FALLBACK_MODELS if m != settings.GEMINI_MODEL]
    last_error = None

    for model_name in models:
        for attempt in range(2):  # 2 tentativas por modelo
            try:
                t0 = time.time()
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=build_config(model_name),
                )

                text = extract_gemini_text(response)
                if not text:
                    reason = None
                    try:
                        reason = response.candidates[0].finish_reason
                    except Exception:
                        pass
                    print(f"[Gemini:{model_name}] resposta vazia | finish_reason={reason} | feedback={getattr(response, 'prompt_feedback', None)}")
                    raise Exception("Resposta vazia do Gemini")

                parsed = json.loads(clean_json_text(text))
                print(f"[Gemini:{model_name}] ok em {time.time() - t0:.1f}s")
                return parsed

            except Exception as e:
                last_error = e
                print(f"[Gemini:{model_name}] tentativa {attempt + 1} falhou: {e}")
                if attempt == 0 and any(m in str(e) for m in RETRY_SAME_MODEL):
                    time.sleep(1)  # sobrecarga temporária: repete uma vez no mesmo modelo
                    continue
                break  # 404, 504/timeout, chave etc.: passa direto para o próximo modelo

    raise Exception(f"Falha na análise do Gemini: {last_error}")


# -----------------------------
# ENGAGEMENT SCORE
# -----------------------------
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


# -----------------------------
# GERAÇÃO DO RESUMO COM RETENTATIVA
# -----------------------------
def generate_inferred_analysis(post_data: dict, caption: str) -> dict:
    """
    Chama o Gemini até 2 vezes. Na segunda tentativa o prompt fica mais rígido
    se o resumo da primeira for só uma cópia da legenda.
    """
    comments = extract_comment_texts(post_data)
    display_url = post_data.get("display_url")

    result = None
    for attempt in range(2):
        prompt = build_inference_prompt(post_data, caption, comments, strict=(attempt == 1))
        result = call_gemini(prompt, image_url=display_url)

        summary = (result.get("summary") or "").strip()
        if len(summary) >= 15 and not is_copy_of_caption(summary, caption):
            return result
        print(f"[Resumo] tentativa {attempt + 1} copiou a legenda ou veio vazio; retentando...")

    return result  # devolve o último resultado mesmo assim


# -----------------------------
# MAIN SERVICE
# -----------------------------
def analyze_post_with_ai(post_data: dict) -> dict:
    caption = clean_text(post_data.get("caption", ""))
    display_url = post_data.get("display_url")
    likes, comments = get_precise_metrics(post_data)
    engagement_score = calculate_engagement(likes, comments)
    viral = classify_virality(engagement_score)

    try:
        ai_result = generate_inferred_analysis(post_data, caption)

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