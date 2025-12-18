from pydantic import BaseModel
from datetime import date

class FoodCreate(BaseModel):
    food_text: str
    calories: float
    protein: float
    date: date

class FoodResponse(BaseModel):
    id: int
    food_text: str
    calories: float
    protein: float
    date: date

    class Config:
        from_attributes = True