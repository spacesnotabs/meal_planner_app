import streamlit as st
from utils import recipe_helper

def show():
    st.header("Recipe Browser")
    st.write("Browse and search for recipes")
    
    # Search box
    search_query = st.text_input("Search recipes", "")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        cuisine = st.multiselect("Cuisine", ["Italian", "Mexican", "Asian", "American"])
    with col2:
        diet = st.multiselect("Diet", ["Vegetarian", "Vegan", "Gluten-Free", "Keto"])
        
    # Recipe cards placeholder
    st.write("Recipe results will appear here")
