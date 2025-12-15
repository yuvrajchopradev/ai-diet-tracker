from fastapi import APIRouter, Depends
from app.schemas.food import FoodResponse, FoodCreate
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.food_entry import FoodEntry

router = APIRouter(prefix="/food", tags=["food"])

@router.post("/", response_model=FoodResponse)
def create_food_entry(
    food: FoodCreate,
    db: Session = Depends(get_db)
):
    entry = FoodEntry(
        food_text = food.food_text,
        calories = food.calories,
        protein = food.protein
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry