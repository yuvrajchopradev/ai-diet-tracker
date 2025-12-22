from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User
from app.auth.security import hash_password
from app.schemas.auth import TokenResponse, LoginRequest
from app.auth.security import verify_password
from app.auth.token import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )

    return new_user

@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token}

@router.get("/me", response_model=UserResponse)
def read_me(current_user = Depends(get_current_user)):
    return current_user