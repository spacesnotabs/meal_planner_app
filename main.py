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

# Sidebar navigation with radio buttons instead of dropdown
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "",  # Empty label since we have a title above
    ["Recipe Browser", "Add Recipe", "Meal Calendar", "Nutrition Tracking"]
)

# Main content
if page == "Recipe Browser":
    recipe_browser.show()
elif page == "Add Recipe":
    recipe_form.show()
elif page == "Meal Calendar":
    calendar.show()
else:
    nutrition_charts.show()