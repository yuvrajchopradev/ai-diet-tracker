from pydantic import BaseModel, Field

class AIEstimateRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Food Description")

class AIEstimationResponse(BaseModel):
    calories: float
    protein: float