from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.food.router import router as food_router
from app.ai.router import router as ai_router

app = FastAPI(title="AI Diet Tracker API")

app.include_router(auth_router)
app.include_router(food_router)
app.include_router(ai_router)

@app.get("/ping")
def ping():
    return {"message": "backend is alive"}