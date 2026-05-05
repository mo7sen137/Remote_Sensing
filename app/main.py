"""
Main Streamlit Application
Remote Sensing Land Classification Dashboard
"""

import streamlit as st
import numpy as np
import os
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessor import RadiometricCalibration
from src.feature_extractor import SpectralIndicesExtractor
from src.classifier import LandClassifier, MultiModelEnsemble
from src.postprocessor import MapGenerator, AccuracyAssessment
from src.utils import LandsatFileHandler, Validator

import config
from app.components import setup_sidebar, setup_main_panel
from app.callbacks import handle_file_upload, run_classification


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Remote Sensing Land Classification",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark theme
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #1a1a2e;
        }
        [data-testid="stMainBlockContainer"] {
            background-color: #16213e;
            color: #eaeaea;
        }
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #0f3460;
        }
        .stButton > button {
            background-color: #e94560;
            color: white;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #ff6b9d;
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main application flow."""
    setup_page_config()
    
    # Title
    st.markdown("# 🛰️ Remote Sensing Land Classification")
    st.markdown("#### Automated Land Cover Mapping from Satellite Imagery")
    
    # Initialize session state
    if 'uploaded_bands' not in st.session_state:
        st.session_state.uploaded_bands = {}
    if 'mtl_data' not in st.session_state:
        st.session_state.mtl_data = None
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = None
    
    # Create columns for layout
    col_sidebar, col_main = st.columns([1, 3])
    
    with col_sidebar:
        st.markdown("### ⚙️ Control Panel")
        st.markdown("---")
        
        # Sidebar controls
        model_name = setup_sidebar()
    
    with col_main:
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📤 Upload Data",
            "🔍 Preview & Indices",
            "🗺️ Classification",
            "📊 Results"
        ])
        
        with tab1:
            setup_main_panel("upload")
        
        with tab2:
            setup_main_panel("preview")
        
        with tab3:
            setup_main_panel("classification", model_name)
        
        with tab4:
            setup_main_panel("results")


if __name__ == "__main__":
    main()
