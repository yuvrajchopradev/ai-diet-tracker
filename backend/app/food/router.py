from fastapi import APIRouter, Depends
from app.schemas.food import FoodResponse, FoodCreate
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.food_entry import FoodEntry
from typing import List
from datetime import date
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/food", tags=["food"])

@router.post("/", response_model=FoodResponse)
def create_food_entry(
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = FoodEntry(
        user_id = current_user.id,
        food_text = food.food_text,
        calories = food.calories,
        protein = food.protein,
        date = food.date
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry

@router.get("/", response_model=List[FoodResponse])
def get_all_food_entries(db: Session = Depends(get_db)):
    return db.query(FoodEntry).all()

@router.get("/by-date", response_model=List[FoodResponse])
def get_food_by_date(
    day: date,
    db: Session = Depends(get_db)
):
    return (
        db.query(FoodEntry)
        .filter(FoodEntry.created_at >= day)
        .filter(FoodEntry.created_at < day.replace(day = day + 1))
        .all()
    )