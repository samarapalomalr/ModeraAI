from pydantic import BaseModel
from typing import List, Optional

# -----------------------------
# REQUEST
# -----------------------------
class AnalyzeRequest(BaseModel):
    post_url: str
    platform: Optional[str] = "instagram"

# -----------------------------
# METRICS
# -----------------------------
class Metrics(BaseModel):
    likes: int = 0
    comments: int = 0

# -----------------------------
# RESPONSE
# -----------------------------
class AnalyzeResponse(BaseModel):
    metrics: Metrics
    display_url: Optional[str] = None  
    engagement_score: float
    viral_classification: str
    content_type: str
    sentiment: str
    summary: Optional[str] = "Resumo não disponível."
    insights: List[str]
    recommendations: List[str]