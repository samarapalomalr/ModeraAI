import re


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def extract_hashtags(text: str):
    return re.findall(r"#\w+", text or "")
