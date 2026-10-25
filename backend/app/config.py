import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    APP_NAME = "Intellux AI Backend"
    DEBUG = True

    def __post_init__(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não definida no .env")


settings = Settings()