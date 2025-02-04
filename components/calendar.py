import streamlit as st
from datetime import datetime, timedelta

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
