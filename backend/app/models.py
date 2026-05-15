# create AIRequest model with:
# id
# feature_name
# model_name
# input_tokens
# output_tokens
# cost
# latency
# created_at
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class AIRequest(Base):
    __tablename__ = "ai_requests"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String, index=True)
    model_name = Column(String)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    cost = Column(Float)
    latency = Column(Float)
    created_at = Column(DateTime)
    engagement_score = Column(Float, default=0)
    retention_score = Column(Float, default=0)
    roi_score = Column(Float, default=0)
