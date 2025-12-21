from app.schemas.ai import AIEstimationResponse

def estimate_food(text: str) -> AIEstimationResponse:
    # Temporary
    return AIEstimationResponse(
        calories=0.0,
        protein=0.0
    )