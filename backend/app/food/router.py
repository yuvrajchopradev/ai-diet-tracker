from fastapi import APIRouter, Depends
from app.schemas.food import FoodResponse, FoodCreate
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.food_entry import FoodEntry
from typing import List
from datetime import date
from app.models.user import User
from app.auth.dependencies import get_current_user
from sqlalchemy import extract

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

@router.get("/months")
def get_food_months(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = (
        db.query(
            extract("year", FoodEntry.date).label("year"),
            extract("month", FoodEntry.date).label("month")
        )
        .filter(FoodEntry.user_id == current_user.id)
        .distinct()
        .order_by("year", "month")
        .all()
    )

    return [
        {"year": int(r.year), "month": (r.month)}
        for r in results
    ]

@router.get("/dates")
def get_food_dates(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = (
        db.query(FoodEntry.date)
        .filter(
            FoodEntry.user_id == current_user.id,
            extract("year", FoodEntry.date) == year,
            extract("month", FoodEntry.date) == month
        )
        .distinct()
        .order_by(FoodEntry.date)
        .all()
    )

    return [r.date for r in results]

@router.get("/day", response_model=List[FoodResponse])
def get_food_for_day(
    day: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(FoodEntry)
        .filter(
            FoodEntry.user_id == current_user.id,
            FoodEntry.date == day
        )
        .order_by(FoodEntry.id)
        .all()
    )