import streamlit as st
from components import calendar, recipe_browser, nutrition_charts, recipe_form
from utils import nutrition, recipe_helper

# Set page config
st.set_page_config(
    page_title="Meal Planner",
    page_icon="🍽️",
    layout="wide"
)

# Title and description
st.title("🍽️ Smart Meal Planner")
st.markdown("""
Plan your meals, track nutrition, and discover new recipes - all in one place!
""")

# Show mini calendar at the top
calendar.mini_calendar()

# Sidebar navigation with standard buttons
st.sidebar.title("Navigation")

# Initialize session state for current page if not exists
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Recipe Browser"

# Navigation buttons
if st.sidebar.button("Recipe Browser", use_container_width=True):
    st.session_state.current_page = "Recipe Browser"
if st.sidebar.button("Add Recipe", use_container_width=True):
    st.session_state.current_page = "Add Recipe"
if st.sidebar.button("Meal Calendar", use_container_width=True):
    st.session_state.current_page = "Meal Calendar"
if st.sidebar.button("Nutrition Tracking", use_container_width=True):
    st.session_state.current_page = "Nutrition Tracking"

# Main content
if st.session_state.current_page == "Recipe Browser":
    recipe_browser.show()
elif st.session_state.current_page == "Add Recipe":
    recipe_form.show()
elif st.session_state.current_page == "Meal Calendar":
    calendar.show()
else:
    nutrition_charts.show()