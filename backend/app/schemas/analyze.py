from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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

class AuditHistoryItem(BaseModel):
    id: int
    platform: str
    target_url: Optional[str] = None
    compliance_score: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AuditDetailResponse(AuditHistoryItem):
    raw_content: Optional[str] = None
    summary: Optional[str] = None
    result_json: str
