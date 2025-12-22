from fastapi import FastAPI
from app.database import engine, Base
from app.auth.router import router as auth_router
from app.food.router import router as food_router
from app.ai.router import router as ai_router

app = FastAPI(title="AI Diet Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(food_router)
app.include_router(ai_router)

@app.get("/health")
def ping():
    return {"status": "ok"}