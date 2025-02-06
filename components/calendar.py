import streamlit as st
from datetime import datetime, timedelta
from models.database import SessionLocal
from models.recipe import Recipe, MealPlan

def mini_calendar(selected_date):
    # Create 3 columns for a more compact view
    cols = st.columns(3)
    
    # Show selected date and next 2 days
    for idx, day_offset in enumerate(range(3)):
        current_date = selected_date + timedelta(days=day_offset)
        with cols[idx]:
            st.markdown(f"**{current_date.strftime('%a, %b %d')}**")
            for meal in ["Breakfast", "Lunch", "Dinner"]:
                meal_key = f"{current_date.strftime('%Y-%m-%d')}_{meal}"
                if meal_key in st.session_state and st.session_state[meal_key] != "Add meal...":
                    st.markdown(f"{meal}: {st.session_state[meal_key]}")
                else:
                    st.markdown(f"{meal}: *Not planned*")

def save_meal_selection(date, meal_type, recipe_name):
    db = SessionLocal()
    try:
        # Delete existing meal plan for this date and meal type
        db.query(MealPlan).filter(
            MealPlan.date == date.strftime('%Y-%m-%d'),
            MealPlan.meal_type == meal_type
        ).delete()
        
        # Update session state immediately
        key = f"{date.strftime('%Y-%m-%d')}_{meal_type}"
        if recipe_name == "Add meal...":
            if key in st.session_state:
                del st.session_state[key]
        else:
            st.session_state[key] = recipe_name
            # Get recipe ID
            recipe = db.query(Recipe).filter(Recipe.name == recipe_name).first()
            if recipe:
                # Create new meal plan
                meal_plan = MealPlan(
                    date=date.strftime('%Y-%m-%d'),
                    meal_type=meal_type,
                    recipe_id=recipe.id
                )
                db.add(meal_plan)
        
        db.commit()
    except Exception as e:
        st.error(f"Error saving meal plan: {str(e)}")
        db.rollback()
    finally:
        db.close()

def load_meal_plans():
    db = SessionLocal()
    try:
        meal_plans = db.query(MealPlan).join(Recipe).all()
        return {
            f"{mp.date}_{mp.meal_type}": mp.recipe.name
            for mp in meal_plans
        }
    except Exception as e:
        st.error(f"Error loading meal plans: {str(e)}")
        return {}
    finally:
        db.close()

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

    # Load existing meal plans
    meal_plans = load_meal_plans()
    
    # Calendar grid
    meals = ["Breakfast", "Lunch", "Dinner"]
    for day in range(7):
        current_date = selected_date + timedelta(days=day)
        st.subheader(current_date.strftime("%A, %B %d"))
        
        cols = st.columns(len(meals))
        for idx, meal in enumerate(meals):
            with cols[idx]:
                st.markdown(f"**{meal}**")
                key = f"{current_date.strftime('%Y-%m-%d')}_{meal}"
                
                # Set initial value from database
                if key not in st.session_state and key in meal_plans:
                    st.session_state[key] = meal_plans[key]
                
                selected_recipe = st.selectbox(
                    "Select recipe",
                    recipe_options,
                    key=key
                )
                
                # Save changes when selection changes
                if key in st.session_state and st.session_state[key] != selected_recipe:
                    save_meal_selection(current_date, meal, selected_recipe)
