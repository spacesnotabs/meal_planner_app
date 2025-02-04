import streamlit as st
from models.database import SessionLocal
from models.recipe import Recipe, SavedIngredient
from typing import List, Dict
import json

def show():
    st.header("Add Custom Recipe")

    # Initialize session
    db = SessionLocal()

    try:
        # Get saved ingredients for dropdown
        saved_ingredients = db.query(SavedIngredient).order_by(SavedIngredient.name).all()
        saved_ingredient_names = [ing.name for ing in saved_ingredients]

        with st.form("recipe_form"):
            # Basic Information
            name = st.text_input("Recipe Name")

            # Cuisine Selection
            cuisines = ["Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian", "Other"]
            cuisine = st.multiselect("Cuisine Type", cuisines)

            # Dietary Preferences
            diets = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Dairy-Free"]
            diet = st.multiselect("Dietary Preferences", diets)

            # Recipe Directions
            directions = st.text_area("Recipe Directions", height=150, 
                                    help="Enter the step-by-step instructions for preparing this recipe")

            # Ingredients
            st.subheader("Ingredients")
            ingredients = []
            num_ingredients = st.number_input("Number of Ingredients", min_value=1, max_value=20, value=3)

            for i in range(int(num_ingredients)):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    # Dropdown for existing ingredients or option to add new
                    ingredient_options = ["Add new ingredient..."] + saved_ingredient_names
                    selected_option = st.selectbox(f"Ingredient {i+1}", 
                                                 ingredient_options,
                                                 key=f"ing_select_{i}")

                    if selected_option == "Add new ingredient...":
                        ingredient_name = st.text_input("New ingredient name", key=f"new_ing_{i}")
                    else:
                        ingredient_name = selected_option

                with col2:
                    amount = st.number_input("Amount (optional)", 
                                           min_value=0.0,
                                           value=0.0,
                                           key=f"ing_amount_{i}")
                with col3:
                    unit = st.selectbox("Unit (optional)",
                                      ["", "g", "ml", "cups", "tbsp", "tsp", "pieces"],
                                      key=f"ing_unit_{i}")
                with col4:
                    include = st.checkbox("Include", value=True, key=f"include_{i}")

                if ingredient_name and include:
                    ingredient_data = {"name": ingredient_name}
                    if amount > 0:
                        ingredient_data["amount"] = amount
                    if unit:
                        ingredient_data["unit"] = unit
                    ingredients.append(ingredient_data)

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
                # Save new ingredients to SavedIngredients table
                for ingredient in ingredients:
                    ing_name = ingredient["name"]
                    if ing_name not in saved_ingredient_names:
                        new_saved_ing = SavedIngredient(
                            name=ing_name,
                            common_unit=ingredient.get("unit", "")
                        )
                        db.add(new_saved_ing)
                        db.commit()

                # Create and save the recipe
                new_recipe = Recipe(
                    name=name,
                    cuisine=cuisine,
                    diet=diet,
                    ingredients=ingredients,
                    directions=directions,
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