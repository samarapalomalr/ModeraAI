import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Autenticação (JWT).
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-change-me")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

    # Configurações de Ambiente e Segurança
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
    DEBUG = ENVIRONMENT != "production"

    # Origens permitidas para CORS (separadas por vírgula no .env)
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
        ).split(",")
        if origin.strip()
    ]

    APP_NAME = "Modera AI Backend"

    def __post_init__(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não definida no .env")
        if self.ENVIRONMENT == "production":
            if not self.JWT_SECRET or self.JWT_SECRET == "dev-insecure-change-me":
                raise ValueError("JWT_SECRET inseguro ou não definido para ambiente de produção!")


settings = Settings()