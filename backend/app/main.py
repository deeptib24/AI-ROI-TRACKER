from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, AIRequest
from app.schemas import AIRequestCreate
from app.schemas import PromptRequest
from app.routes import analytics

app = FastAPI()
app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "AI ROI Tracker Backend Running"}

@app.post("/track-ai-request")
def track_ai_request(
    request: AIRequestCreate,
    db: Session = Depends(get_db)
):
    new_request = AIRequest(
        feature_name=request.feature_name,
        model_name=request.model_name,
        input_tokens=request.input_tokens,
        output_tokens=request.output_tokens,
        cost=request.cost,
        latency=request.latency
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "AI request stored successfully",
        "id": new_request.id
    }

from app.services.groq_service import generate_ai_response

@app.get("/test-ai")
def test_ai():

    result = generate_ai_response(
        "Explain AI in one sentence"
    )

    return result

@app.post("/generate-ai")
def generate_ai(
    request: PromptRequest,
    db: Session = Depends(get_db)
):

    result = generate_ai_response(request.prompt)

    ai_message = result["choices"][0]["message"]["content"]

    prompt_tokens = result["usage"]["prompt_tokens"]
    completion_tokens = result["usage"]["completion_tokens"]

    total_cost = (
        prompt_tokens * 0.000001 +
        completion_tokens * 0.000002
    )
    roi_score = (
    request.retention_score - total_cost
    ) / total_cost
    roi_score = round(min(roi_score, 50), 2)
    new_request = AIRequest(
        feature_name=request.feature_name,
        model_name="llama-3.1-8b-instant",
        input_tokens=prompt_tokens,
        output_tokens=completion_tokens,
        cost=total_cost,
        latency=0.0,
        engagement_score=request.engagement_score,
        retention_score=request.retention_score,
        roi_score=roi_score,
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {
        "response": ai_message,
        "tokens": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens
        },
        "cost": total_cost
    }