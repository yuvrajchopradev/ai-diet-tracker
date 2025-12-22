from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.schemas.food import FoodResponse, FoodCreate
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.food_entry import FoodEntry
from typing import List
from datetime import date
from app.models.user import User
from app.auth.dependencies import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/food", tags=["food"])

@router.post("/", response_model=FoodResponse, status_code=status.HTTP_201_CREATED)
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

    try:
        db.add(entry)
        db.commit()
        db.refresh(entry)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )

    return entry

@router.get("/", response_model=List[FoodResponse])
def get_all_food_entries(db: Session = Depends(get_db)):
    return db.query(FoodEntry).all()

@router.get("/months")
def get_food_months(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = (
        db.query(
            func.extract("year", FoodEntry.date).label("year"),
            func.extract("month", FoodEntry.date).label("month")
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
            func.extract("year", FoodEntry.date) == year,
            func.extract("month", FoodEntry.date) == month
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

@router.get("/summary/day")
def day_summary(
    date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = (
        db.query(
            func.coalesce(func.sum(FoodEntry.calories), 0),
            func.coalesce(func.sum(FoodEntry.protein), 0),
        )
        .filter(
            FoodEntry.user_id == current_user.id,
            FoodEntry.date == date,
        )
        .one()
    )

    return {
        "date": date,
        "total_calories": result[0],
        "total_protein": result[1],
    }

@router.get("/summary/month")
def month_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    result = (
        db.query(
            func.coalesce(func.sum(FoodEntry.calories), 0),
            func.coalesce(func.sum(FoodEntry.protein), 0),
        )
        .filter(
            FoodEntry.user_id == current_user.id,
            func.extract("year", FoodEntry.date) == year,
            func.extract("month", FoodEntry.date) == month
        )
        .one()
    )

    return {
        "year": year,
        "month": month,
        "total_calories": result[0],
        "total_protein": result[1],
    }

@router.get("/summary/month/days")
def month_day_breakdown(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    results = (
        db.query(
            FoodEntry.date,
            func.sum(FoodEntry.calories).label("calories"),
            func.sum(FoodEntry.protein).label("protein"),
        )
        .filter(
            FoodEntry.user_id == current_user.id,
            func.extract("year", FoodEntry.date) == year,
            func.extract("month", FoodEntry.date) == month,
        )
        .group_by(FoodEntry.date)
        .order_by(FoodEntry.date)
        .all()
    )

    return [
        {
            "date": r.date,
            "total_calories": r.calories,
            "total_protein": r.protein,
        }
        for r in results
    ]