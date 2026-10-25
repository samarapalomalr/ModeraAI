from pydantic import BaseModel
from typing import List, Optional

# -----------------------------
# REQUEST
# -----------------------------
class AnalyzeRequest(BaseModel):
    post_url: str

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
    insights: List[str]
    recommendations: List[str]