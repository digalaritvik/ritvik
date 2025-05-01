import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Kota Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Kota Analysis Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis", "Visualization", "Reports"])

# Main content
if page == "Home":
    st.header("Welcome to Kota Analysis")
    st.write("This dashboard provides analysis and insights about Kota.")
    
elif page == "Data Analysis":
    st.header("Data Analysis")
    st.write("Perform data analysis here.")
    
elif page == "Visualization":
    st.header("Data Visualization")
    st.write("Create visualizations here.")
    
elif page == "Reports":
    st.header("Reports")
    st.write("Generate and view reports here.")

# Footer
st.markdown("---")
st.caption("© 2024 Kota Analysis Dashboard") 