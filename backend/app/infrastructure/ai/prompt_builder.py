"""Montagem do prompt e extração de dados para a IA."""
import re

from app.utils.helpers import clean_text, to_int

def extract_comment_texts(post_data: dict, limit: int = 30) -> list[str]:
    """
    Extrai o texto dos comentários, se o scraper os repassar.
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
    total_comments = to_int(post_data.get("comments", 0))

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
