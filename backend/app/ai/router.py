from fastapi import APIRouter, Depends
from app.schemas.ai import AIEstimateRequest, AIEstimationResponse
from app.ai.service import estimate_food
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/estimate", response_model=AIEstimationResponse)
def estimate(payload: AIEstimateRequest, current_user = Depends(get_current_user)):
    return estimate_food(payload.text)