import streamlit as st
from models.database import SessionLocal
from models.recipe import Recipe
from typing import List, Dict

def show():
    st.header("Recipe Browser")
    st.write("Browse and search for recipes")

    # Initialize database session
    db = SessionLocal()

    try:
        # Search box
        search_query = st.text_input("Search recipes", "")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            cuisine = st.multiselect("Cuisine", ["Italian", "Mexican", "Asian", "American"])
        with col2:
            diet = st.multiselect("Diet", ["Vegetarian", "Vegan", "Gluten-Free", "Keto"])

        # Query recipes
        query = db.query(Recipe)

        # Apply filters
        if search_query:
            query = query.filter(Recipe.name.ilike(f"%{search_query}%"))
        if cuisine:
            query = query.filter(Recipe.cuisine.contains(cuisine))
        if diet:
            query = query.filter(Recipe.diet.contains(diet))

        recipes = query.all()

        # Display recipes
        if recipes:
            for recipe in recipes:
                with st.expander(f"📖 {recipe.name}"):
                    st.write(f"**Cuisine:** {', '.join(recipe.cuisine)}")
                    st.write(f"**Diet:** {', '.join(recipe.diet)}")

                    st.subheader("Ingredients")
                    for ingredient in recipe.ingredients:
                        ingredient_text = f"• {ingredient['name']}"
                        if 'amount' in ingredient and 'unit' in ingredient:
                            ingredient_text += f": {ingredient['amount']} {ingredient['unit']}"
                        elif 'amount' in ingredient:
                            ingredient_text += f": {ingredient['amount']}"
                        elif 'unit' in ingredient:
                            ingredient_text += f": {ingredient['unit']}"
                        st.write(ingredient_text)

                    if recipe.directions:
                        st.subheader("Directions")
                        st.write(recipe.directions)

                    st.subheader("Nutrition Information")
                    cols = st.columns(5)
                    cols[0].metric("Calories", f"{recipe.calories:.0f} kcal")
                    cols[1].metric("Protein", f"{recipe.protein:.1f}g")
                    cols[2].metric("Carbs", f"{recipe.carbs:.1f}g")
                    cols[3].metric("Fat", f"{recipe.fat:.1f}g")
                    cols[4].metric("Fiber", f"{recipe.fiber:.1f}g")
        else:
            st.info("No recipes found. Try adjusting your search criteria or add some recipes!")

    except Exception as e:
        st.error(f"An error occurred while loading recipes: {str(e)}")
    finally:
        db.close()