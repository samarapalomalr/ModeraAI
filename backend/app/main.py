from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database.session import engine, Base
from app.api.routes.analyze import router as analyze_router
from app.api.routes.media import router as media_router
from app.api.routes.auth import router as auth_router
from app.core.config import settings
import app.infrastructure.database.models

# Cria o arquivo moderaai.db automaticamente caso nao exista
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modera AI Backend",
    description="API para análise de posts do Instagram com IA generativa",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
# Se em produção ou origins configuradas, restringe. Senão, aceita localhost/dev.
origins = ["*"] if settings.DEBUG and "*" in settings.ALLOWED_ORIGINS else settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTES
# -----------------------------
app.include_router(analyze_router)
app.include_router(media_router)
app.include_router(auth_router)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Modera API rodando 🚀"
    }
