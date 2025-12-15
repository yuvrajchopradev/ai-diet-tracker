from pydantic import BaseModel

class FoodCreate(BaseModel):
    food_text: str
    calories: float | None = None
    protein: float | None = None

class FoodResponse(BaseModel):
    id: int
    food_text: str
    calories: float | None
    protein: float | None

    class Config:
        from_attributes = True