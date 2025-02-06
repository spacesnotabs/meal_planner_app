import streamlit as st
from datetime import datetime, timedelta
from models.database import SessionLocal
from models.recipe import Recipe

def mini_calendar(selected_date):
    # Create 3 columns for a more compact view
    cols = st.columns(3)
    
    # Show selected date and next 2 days
    for idx, day_offset in enumerate(range(3)):
        current_date = selected_date + timedelta(days=day_offset)
        with cols[idx]:
            st.markdown(f"**{current_date.strftime('%a, %b %d')}**")
            for meal in ["🌅 Breakfast", "🌞 Lunch", "🌙 Dinner"]:
                meal_key = f"{current_date.strftime('%Y-%m-%d')}_{meal}"
                if meal_key in st.session_state and st.session_state[meal_key] != "Add meal...":
                    st.markdown(f"{meal}: {st.session_state[meal_key]}")
                else:
                    st.markdown(f"{meal}: *Not planned*")

def show():
    st.header("Meal Calendar")
    st.write("Plan your meals for the week")
    
    # Date selection
    selected_date = st.date_input("Select week starting from", datetime.now())
    
    # Show mini calendar at the top of the calendar page
    st.markdown("### Next 3 Days Overview")
    mini_calendar(selected_date)
    
    st.markdown("---")
    st.markdown("### Weekly Plan")
    
    # Get recipe options from database
    db = SessionLocal()
    try:
        recipes = db.query(Recipe).order_by(Recipe.name).all()
        recipe_options = ["Add meal..."] + [recipe.name for recipe in recipes]
    except Exception as e:
        st.error(f"Error loading recipes: {str(e)}")
        recipe_options = ["Add meal..."]
    finally:
        db.close()
    
    # Calendar grid
    meals = ["Breakfast", "Lunch", "Dinner"]
    for day in range(7):
        current_date = selected_date + timedelta(days=day)
        st.subheader(current_date.strftime("%A, %B %d"))
        
        cols = st.columns(len(meals))
        for idx, meal in enumerate(meals):
            with cols[idx]:
                st.markdown(f"**{meal}**")
                selected_recipe = st.selectbox(
                    "Select recipe",
                    recipe_options,
                    key=f"{current_date.strftime('%Y-%m-%d')}_{meal}"
                )
