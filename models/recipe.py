from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cuisine = Column(JSON)  # Store as JSON array
    diet = Column(JSON)     # Store as JSON array
    ingredients = Column(JSON)  # Store ingredients as JSON
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # Store as YYYY-MM-DD
    meal_type = Column(String)  # Breakfast, Lunch, or Dinner
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe")
