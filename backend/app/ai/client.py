from google import genai
from google.genai import types
from app.ai.prompts import SYSTEM_PROMPT
from app.core.config import settings
from app.schemas.ai import AIEstimationResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)

generation_config = types.GenerateContentConfig(
    max_output_tokens=500,
    system_instruction=SYSTEM_PROMPT,
    response_mime_type="application/json",
    response_json_schema=AIEstimationResponse.model_json_schema()
)