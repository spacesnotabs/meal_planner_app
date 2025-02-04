import streamlit as st
from utils import nutrition

def show():
    st.header("Nutrition Tracking")
    st.write("Monitor your nutritional intake")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From")
    with col2:
        end_date = st.date_input("To")
        
    # Placeholder for nutrition charts
    st.write("Nutrition charts will appear here")
    
    # Summary statistics
    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Calories", "2000 kcal")
    with col2:
        st.metric("Protein", "75g")
    with col3:
        st.metric("Carbs", "250g")
