from fastapi import APIRouter

from app.api.routes import analyze, audits, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(analyze.router)
api_router.include_router(audits.router)
