from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, default="instagram")
    target_url = Column(String(500), nullable=True)
    raw_content = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="COMPLETED")
    summary = Column(Text, nullable=True)
    compliance_score = Column(Integer, nullable=True)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
