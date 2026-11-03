import os
from dotenv import load_dotenv

load_dotenv()


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    APP_NAME = "Modera AI Backend"
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    # Integrações externas
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Banco de dados (SQLite por padrão)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./moderaai.db")

    # CORS: lista separada por vírgulas. "*" libera tudo.
    CORS_ORIGINS = _split_csv(os.getenv("CORS_ORIGINS", "*"))

    def __post_init__(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não definida no .env")


settings = Settings()
