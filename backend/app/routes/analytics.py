from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import AIRequest

router = APIRouter()

@router.get("/total-cost")
def total_cost(db: Session = Depends(get_db)):

    total = db.query(
        func.sum(AIRequest.cost)
    ).scalar()

    return {
        "total_ai_cost": total or 0
    }

@router.get("/total-tokens")
def total_tokens(db: Session = Depends(get_db)):

    total = db.query(
        func.sum(
            AIRequest.input_tokens +
            AIRequest.output_tokens
        )
    ).scalar()

    return {
        "total_tokens": total or 0
    }

@router.get("/top-features")
def top_features(db: Session = Depends(get_db)):

    results = db.query(
        AIRequest.feature_name,
        func.sum(AIRequest.cost).label("total_cost")
    ).group_by(
        AIRequest.feature_name
    ).all()

    formatted_results = []

    for feature_name, total_cost in results:

        formatted_results.append({
            "feature_name": feature_name,
            "total_cost": total_cost
        })

    return formatted_results

@router.get("/cost-by-feature")
def cost_by_feature(db: Session = Depends(get_db)):

    results = db.query(
        AIRequest.feature_name,
        func.sum(AIRequest.cost).label("total_cost")
    ).group_by(
        AIRequest.feature_name
    ).all()

    formatted_results = []

    for feature_name, total_cost in results:

        formatted_results.append({
            "feature_name": feature_name,
            "total_cost": float(total_cost)
        })

    return formatted_results

@router.get("/roi-by-feature")
def roi_by_feature(db: Session = Depends(get_db)):

    results = db.query(
        AIRequest.feature_name,
        func.avg(AIRequest.roi_score).label("avg_roi")
    ).group_by(
        AIRequest.feature_name
    ).all()

    formatted_results = []

    for feature_name, avg_roi in results:

        formatted_results.append({
            "feature_name": feature_name,
            "avg_roi": float(avg_roi)
        })

    return formatted_results