# create FastAPI POST route for AI request
# accepts:
# prompt
# feature_name
# sends request to Groq API
# logs tokens and cost
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import AIRequest
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/ai/request")
def log_ai_request(feature_name: str, model_name: str, input_tokens: int, output_tokens: int, cost: float, latency: float, db: Session = Depends(get_db)):
    ai_request = AIRequest(
        feature_name=feature_name,
        model_name=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
        latency=latency
    )
    db.add(ai_request)
    db.commit()
    db.refresh(ai_request)
    return {"message": "AI request logged successfully", "request_id": ai_request.id}
