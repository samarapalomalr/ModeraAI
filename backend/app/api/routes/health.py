from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    return {"status": "ok", "message": "Modera API rodando 🚀"}
