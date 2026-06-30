import streamlit as st

st.set_page_config(layout="wide", page_title="Cyclone Prediction Home", page_icon="🏠")

st.title("🌪️ Comparative Analysis of ML & DL Techniques for Cyclone Prediction")
st.image("https://images.unsplash.com/photo-1594225095383-73516848072d?w=800", use_column_width=True)

st.markdown("---")
st.header("About This Project")
st.write("""
This application provides a comprehensive platform for weather prediction. 
It uses advanced machine learning algorithms to analyze atmospheric data 
and accurately forecast weather conditions such as temperature, rainfall, 
humidity, and wind patterns.
""")


st.info("Please **Login** or **Sign Up** using the navigation sidebar on the left to access the prediction dashboard.")