import json
from app.schemas.ai import AIEstimationResponse
from app.ai.client import client, generation_config

def estimate_food(text: str) -> AIEstimationResponse:
    prompt = f"Food description: {text}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=generation_config
        )

        data = json.loads(response.text.strip())

        calories = float(data["calories"])
        protein = float(data["protein"])

        if calories < 0 or protein < 0:
            raise ValueError("Negative values are not allowed")
        
        return AIEstimationResponse(
            calories=calories,
            protein=protein
        )
    except Exception as e:
        print(f"[AI ERROR] {e}")
        return AIEstimationResponse(
            calories=0.0,
            protein=0.0,
        )