from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.analyze import router as analyze_router
import app.models

# Cria o arquivo moderaai.db automaticamente caso nao exista
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intellux AI Backend",
    description="API para análise de posts do Instagram com IA generativa",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTES
# -----------------------------
app.include_router(analyze_router)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Intellux API rodando 🚀"
    }
