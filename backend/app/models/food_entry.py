from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_text = Column(String, nullable=False)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="food_entries")