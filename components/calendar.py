import streamlit as st
from datetime import datetime, timedelta

def mini_calendar():
    # Get today's date
    today = datetime.now()
    
    # Create 3 columns for a more compact view
    cols = st.columns(3)
    
    # Show next 3 days including today
    for idx, day_offset in enumerate(range(3)):
        current_date = today + timedelta(days=day_offset)
        with cols[idx]:
            st.markdown(f"**{current_date.strftime('%a, %b %d')}**")
            for meal in ["🌅 Breakfast", "🌞 Lunch", "🌙 Dinner"]:
                meal_key = f"mini_{current_date.strftime('%Y-%m-%d')}_{meal}"
                if meal_key in st.session_state:
                    st.markdown(f"{meal}: {st.session_state[meal_key]}")
                else:
                    st.markdown(f"{meal}: *Not planned*")

def show():
    st.header("Meal Calendar")
    st.write("Plan your meals for the week")
    
    # Date selection
    selected_date = st.date_input("Select week starting from", datetime.now())
    
    # Calendar grid
    meals = ["Breakfast", "Lunch", "Dinner"]
    for day in range(7):
        current_date = selected_date + timedelta(days=day)
        st.subheader(current_date.strftime("%A, %B %d"))
        
        for meal in meals:
            st.text(f"{meal}:")
            st.selectbox(
                "Select recipe",
                ["Add meal..."],
                key=f"{current_date}_{meal}"
            )
