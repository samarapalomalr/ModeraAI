import json
import re
import time

import requests
from google import genai
from google.genai import types

# Modelos alternativos (usados quando o principal responde 503/429 por alta demanda).
FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]
RETRY_SAME_MODEL = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")  # sobrecarga: espera e repete

# Em moderação o modelo precisa poder LER conteúdo ofensivo sem ser bloqueado.
SAFETY_CATEGORIES = (
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
)


def _extract_text(response) -> str | None:
    try:
        return response.text
    except Exception as e:
        print(f"[Gemini parse error]: {e}")
        return None


def _clean_json_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if "```" in text:
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


class GeminiClient:
    """Wrapper do SDK Gemini: monta a requisição, faz retry e fallback de modelos."""

    def __init__(self, api_key: str | None, model: str, timeout_ms: int = 30000):
        self._client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=timeout_ms),
        )
        self._model = model

    @staticmethod
    def _load_image_part(image_url: str):
        try:
            res = requests.get(image_url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                mime = res.headers.get("Content-Type", "image/jpeg").split(";")[0]
                if not mime.startswith("image/"):
                    mime = "image/jpeg"
                return types.Part.from_bytes(data=res.content, mime_type=mime)
        except Exception as img_err:
            print(f"[Aviso]: Imagem não carregada para o Gemini: {img_err}")
        return None

    @staticmethod
    def _build_config(model_name: str) -> types.GenerateContentConfig:
        # Gemini 3.x controla o raciocínio por "thinking_level"; o 2.5 usa "thinking_budget".
        if model_name.startswith("gemini-2.5"):
            thinking = types.ThinkingConfig(thinking_budget=0)
        else:
            thinking = types.ThinkingConfig(thinking_level="low")
        safety = [types.SafetySetting(category=c, threshold="BLOCK_NONE") for c in SAFETY_CATEGORIES]
        return types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=2048,
            thinking_config=thinking,
            safety_settings=safety,
        )

    def generate_json(self, prompt: str, image_url: str | None = None) -> dict:
        contents = [prompt]
        if image_url:
            part = self._load_image_part(image_url)
            if part:
                contents.append(part)

        models = [self._model] + [m for m in FALLBACK_MODELS if m != self._model]
        last_error = None

        for model_name in models:
            for attempt in range(2):  # 2 tentativas por modelo
                try:
                    t0 = time.time()
                    response = self._client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=self._build_config(model_name),
                    )

                    text = _extract_text(response)
                    if not text:
                        reason = None
                        try:
                            reason = response.candidates[0].finish_reason
                        except Exception:
                            pass
                        print(f"[Gemini:{model_name}] resposta vazia | finish_reason={reason} | feedback={getattr(response, 'prompt_feedback', None)}")
                        raise Exception("Resposta vazia do Gemini")

                    parsed = json.loads(_clean_json_text(text))
                    print(f"[Gemini:{model_name}] ok em {time.time() - t0:.1f}s")
                    return parsed

                except Exception as e:
                    last_error = e
                    print(f"[Gemini:{model_name}] tentativa {attempt + 1} falhou: {e}")
                    if attempt == 0 and any(m in str(e) for m in RETRY_SAME_MODEL):
                        time.sleep(1)  # sobrecarga temporária: repete uma vez no mesmo modelo
                        continue
                    break  # 404, 504/timeout, chave etc.: passa para o próximo modelo

        raise Exception(f"Falha na análise do Gemini: {last_error}")
