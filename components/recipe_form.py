import streamlit as st
from models.database import SessionLocal
from models.recipe import Recipe
from typing import List, Dict
import json

def show():
    st.header("Add Custom Recipe")
    
    # Initialize session
    db = SessionLocal()
    
    try:
        with st.form("recipe_form"):
            # Basic Information
            name = st.text_input("Recipe Name")
            
            # Cuisine Selection
            cuisines = ["Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian", "Other"]
            cuisine = st.multiselect("Cuisine Type", cuisines)
            
            # Dietary Preferences
            diets = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Dairy-Free"]
            diet = st.multiselect("Dietary Preferences", diets)
            
            # Ingredients
            st.subheader("Ingredients")
            ingredients = []
            num_ingredients = st.number_input("Number of Ingredients", min_value=1, max_value=20, value=3)
            
            for i in range(int(num_ingredients)):
                col1, col2, col3 = st.columns(3)
                with col1:
                    ingredient_name = st.text_input(f"Ingredient {i+1}", key=f"ing_name_{i}")
                with col2:
                    amount = st.number_input(f"Amount", min_value=0.1, key=f"ing_amount_{i}")
                with col3:
                    unit = st.selectbox(f"Unit", ["g", "ml", "cups", "tbsp", "tsp", "pieces"], key=f"ing_unit_{i}")
                
                if ingredient_name:
                    ingredients.append({
                        "name": ingredient_name,
                        "amount": amount,
                        "unit": unit
                    })
            
            # Nutrition Information
            st.subheader("Nutrition Information (per serving)")
            col1, col2 = st.columns(2)
            with col1:
                calories = st.number_input("Calories", min_value=0)
                protein = st.number_input("Protein (g)", min_value=0.0)
                carbs = st.number_input("Carbohydrates (g)", min_value=0.0)
            with col2:
                fat = st.number_input("Fat (g)", min_value=0.0)
                fiber = st.number_input("Fiber (g)", min_value=0.0)
            
            # Submit button
            submitted = st.form_submit_button("Add Recipe")
            
            if submitted:
                new_recipe = Recipe(
                    name=name,
                    cuisine=cuisine,
                    diet=diet,
                    ingredients=ingredients,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                    fiber=fiber
                )
                
                db.add(new_recipe)
                db.commit()
                st.success("Recipe added successfully!")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        db.close()
