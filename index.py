import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from App_fixed import *

if __name__ == "__main__":
    # Set page config
    st.set_page_config(
        page_title="Resume AI Analyzer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the main application
    run()
