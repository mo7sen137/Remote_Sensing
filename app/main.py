"""
Main Streamlit Application
Remote Sensing Land Classification Dashboard

Complete UI with:
- Data Upload
- Visualization
- Classification
- Results Display
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import os
from pathlib import Path
import json

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


# ============================================================================
# 🎨 PAGE CONFIGURATION
# ============================================================================

def setup_page_config():
    """Configure Streamlit page settings with Professional Enterprise Theme."""
    st.set_page_config(
        page_title="🛰️ Remote Sensing Land Classification",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # =========================================================================
    # PROFESSIONAL DARK THEME - CLEAN & WORKING v5.0
    # =========================================================================
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Icons');
        
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes floatAnim {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        
        :root {
            --primary: #8B5CF6;
            --accent: #A78BFA;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            --bg-dark: #0F0F1E;
            --bg-card: #1A1A2E;
            --bg-card-light: #252541;
            --border: #3F3F5F;
            --text-primary: #E8E8F0;
            --text-secondary: #B0B0C0;
        }
        
        /* Root app background */
        .stApp {
            background: linear-gradient(-45deg, #0F0F1E, #1A0F2E, #0A0A14, #250F3E);
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A1A2E 0%, #252541 100%) !important;
            border-right: 2px solid var(--primary) !important;
        }
        
        /* Main content area */
        [data-testid="stMainBlockContainer"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
        }
        
        [data-testid="stAppViewBlockContainer"] {
            background-color: transparent !important;
        }
        
        /* Headers */
        h1 {
            color: var(--primary) !important;
            font-weight: 700 !important;
            font-size: 38px !important;
            line-height: 1.2 !important;
            margin-bottom: 16px !important;
            text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }
        
        h2 {
            color: var(--accent) !important;
            font-weight: 600 !important;
            font-size: 28px !important;
            line-height: 1.3 !important;
            margin-bottom: 16px !important;
        }
        
        h3 {
            color: var(--accent) !important;
            font-weight: 600 !important;
            font-size: 20px !important;
            line-height: 1.4 !important;
            margin-bottom: 8px !important;
        }
        
        /* Body text */
        p, body, span {
            color: var(--text-primary) !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
        }
        
        /* Font family - exclude icons */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
        }
        
        /* Material Icons specific */
        .material-icons,
        [role="img"],
        button [role="img"],
        [data-testid="collapsedControl"] *,
        [data-testid="collapsedControl"] button * {
            font-family: 'Material Icons' !important;
        }
        
        /* Divider */
        hr {
            border: 0 !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--primary), transparent) !important;
            margin: 24px 0 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
            color: white !important;
            border: 1px solid var(--primary) !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--accent), var(--primary)) !important;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Cards */
        .card {
            background: linear-gradient(135deg, #1A1A2E 0%, #252541 100%) !important;
            border: 1px solid var(--primary) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin: 16px 0 !important;
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        .card:hover {
            background: linear-gradient(135deg, #252541 0%, #2F1F4E 100%) !important;
            box-shadow: 0 12px 48px rgba(139, 92, 246, 0.3) !important;
            border-color: var(--accent) !important;
            transform: translateY(-4px) !important;
        }
        
        /* Card variants */
        .card-accent {
            border-left: 4px solid var(--primary) !important;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(167, 139, 250, 0.05) 100%) !important;
        }
        
        .card-success {
            border-left: 4px solid var(--success) !important;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1A1A2E 0%, #252541 100%) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            padding: 16px !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stMetric"]:hover {
            border-color: var(--primary) !important;
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.25) !important;
        }
        
        /* Markdown container */
        [data-testid="stMarkdownContainer"] {
            color: var(--text-primary) !important;
        }
        
        /* Expander */
        [data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.5), rgba(37, 37, 65, 0.5)) !important;
        }
        
        /* File uploader */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed var(--primary) !important;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), rgba(167, 139, 250, 0.02)) !important;
        }
        
        /* Success message */
        .stSuccess {
            background-color: rgba(16, 185, 129, 0.15) !important;
            color: #10B981 !important;
            border: 1px solid #10B981 !important;
            border-radius: 8px !important;
        }
        
        /* Warning message */
        .stWarning {
            background-color: rgba(245, 158, 11, 0.15) !important;
            color: #F59E0B !important;
            border: 1px solid #F59E0B !important;
            border-radius: 8px !important;
        }
        
        /* Team member card */
        .team-member {
            background: rgba(139, 92, 246, 0.1) !important;
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
            border-radius: 6px !important;
            padding: 10px !important;
            margin: 6px 0 !important;
            font-size: 13px !important;
            color: #B0B0C0 !important;
        }
        
        .team-member:hover {
            background: rgba(139, 92, 246, 0.15) !important;
            color: #C0C0D0 !important;
        }
        
        /* Column */
        [data-testid="column"] {
            background-color: transparent !important;
        }
        
        /* Divider color */
        .stDivider {
            background: linear-gradient(90deg, transparent, var(--primary), transparent) !important;
        }
        
        /* Input fields */
        input[type="text"],
        input[type="password"],
        textarea,
        select {
            background: linear-gradient(135deg, #1A1A2E 0%, #252541 100%) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
        }
        
        /* Radio button */
        [role="radio"] {
            color: var(--primary) !important;
        }
        
        /* Checkbox */
        [role="checkbox"] {
            color: var(--primary) !important;
        }
        
        /* Sidebar toggle button - don't interfere */
        [data-testid="collapsedControl"] {
            /* Keep default styling */
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 📄 PAGE 1: HOME
# ============================================================================

def page_home():
    """Home page with project overview."""
    st.markdown("<h1 style='text-align: center; margin-bottom: 8px;'>Remote Sensing Classification</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--text-secondary); font-size: 16px; margin-bottom: 24px;'>Advanced satellite imagery processing with machine learning</p>", unsafe_allow_html=True)
    st.divider()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.metric("Satellite", "Landsat 8", "11 Bands")
    with col2:
        st.metric("Resolution", "30 meters", "Per pixel")
    with col3:
        st.metric("ML Models", "3 Types", "Ensemble voting")
    with col4:
        st.metric("Classes", "4", "Land cover types")
    
    st.divider()
    
    # Main Content
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>Project Overview</h3>
            <p>Satellite imagery classification from Landsat 8 covering Egypt's Nile Delta region.</p>
            <p style='font-weight: 600; margin-bottom: 8px;'>Land Cover Types:</p>
            <ul style='margin: 0; padding-left: 20px;'>
            <li>Water - Lakes, rivers, and coastal areas</li>
            <li>Agriculture - Cultivated vegetation</li>
            <li>Urban - Buildings and infrastructure</li>
            <li>Desert - Bare soil and sand</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card card-success'>
            <h3 style='margin-top: 0;'>Processing Workflow</h3>
            <p style='margin-bottom: 12px;'>5-step automated pipeline:</p>
            <ol style='margin: 0; padding-left: 20px;'>
            <li>Upload Landsat 8 bands</li>
            <li>Extract spectral indices</li>
            <li>Select ML classifier</li>
            <li>Generate classification map</li>
            <li>Export results and statistics</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Technical Specs
    st.markdown("<h2 style='text-align: center; margin-bottom: 24px;'>System Specifications</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        with st.expander("Preprocessing & Calibration", expanded=False):
            st.markdown("""
            • Radiometric calibration
            • Band normalization
            • Quality filtering
            • Geometric validation
            """)
    
    with col2:
        with st.expander("Feature Extraction", expanded=False):
            st.markdown("""
            **Input Bands:**
            B2 through B7 (6 bands)
            
            **Computed Indices:**
            • NDVI (vegetation)
            • NDWI (water)
            • NDBI (urban)
            """)
    
    with col3:
        with st.expander("ML Classification", expanded=False):
            st.markdown("""
            **Ensemble Models:**
            • Random Forest
            • Support Vector Machine
            • K-Nearest Neighbors
            
            **Voting:** Majority voting
            """)
    
    st.divider()
    
    st.markdown("""
    <div class='card'>
        <h3 style='text-align: center; margin-top: 0;'>Ready to Get Started?</h3>
        <p style='text-align: center; margin-bottom: 0;'>Navigate to the Upload tab to begin processing your satellite imagery</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 📤 PAGE 2: UPLOAD DATA
# ============================================================================

def page_upload():
    """Data upload interface."""
    st.markdown("<h1>Upload Satellite Data</h1>", unsafe_allow_html=True)
    st.markdown("<p>Import Landsat 8 bands and MTL metadata</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h3>Spectral Bands (B2-B7)</h3>", unsafe_allow_html=True)
    
    uploaded_bands = {}
    col1, col2, col3 = st.columns(3)
    
    for band_num in range(2, 8):
        col = col1 if band_num < 5 else (col2 if band_num < 6 else col3)
        with col:
            uploaded_file = st.file_uploader(
                f"Band {band_num}",
                type=['tif', 'tiff'],
                key=f"band_{band_num}"
            )
            if uploaded_file:
                uploaded_bands[band_num] = uploaded_file
    
    if uploaded_bands:
        st.session_state.uploaded_bands = uploaded_bands
    
    st.markdown("<h3>Metadata File</h3>", unsafe_allow_html=True)
    
    mtl_file = st.file_uploader(
        "MTL File",
        type=['txt'],
        key="mtl_file"
    )
    
    if mtl_file:
        st.session_state.mtl_data = mtl_file
        st.success("✅ Metadata file loaded")
    
    st.divider()
    
    # Show file sizes
    if uploaded_bands or mtl_file:
        st.markdown("<h2>Upload Summary</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            status = "Complete" if len(uploaded_bands) == 6 else "Incomplete"
            st.metric("Bands Loaded", f"{len(uploaded_bands)}/6", delta=status)
        
        with col2:
            mtl_status = "Ready" if mtl_file else "Missing"
            st.metric("MTL File", "Loaded" if mtl_file else "Not Loaded", delta=mtl_status)
        
        with col3:
            ready = "Ready" if len(uploaded_bands) == 6 and mtl_file else "Waiting"
            st.metric("Processing", "Can Start" if len(uploaded_bands) == 6 and mtl_file else "Incomplete", delta=ready)


# ============================================================================
# 🔍 PAGE 3: PREVIEW & ANALYSIS
# ============================================================================

def page_preview():
    """Data preview and spectral analysis."""
    st.markdown("# Data Preview & Analysis")
    
    if not st.session_state.uploaded_bands:
        st.warning("Please upload bands first in the Upload Data tab")
        return
    
    st.markdown("## Band Information")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("### Available Bands")
        for band_num in st.session_state.uploaded_bands.keys():
            st.text(f"✓ Band {band_num}")
    
    with col2:
        st.markdown("### Spectral Indices")
        st.text("• NDVI - Vegetation")
        st.text("• NDWI - Water")
        st.text("• NDBI - Urban")
    
    with col3:
        st.markdown("### Processing Steps")
        st.text("1. Radiometric Calibration")
        st.text("2. Indices Calculation")
        st.text("3. ML Classification")
    
    st.markdown("---")
    
    # Show formulas
    st.markdown("## Spectral Indices Formulas")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        ### NDVI
        $$NDVI = \\frac{NIR - Red}{NIR + Red}$$
        
        Vegetation index
        """)
    
    with col2:
        st.markdown("""
        ### NDWI
        $$NDWI = \\frac{NIR - SWIR1}{NIR + SWIR1}$$
        
        Water index
        """)
    
    with col3:
        st.markdown("""
        ### NDBI
        $$NDBI = \\frac{SWIR1 - NIR}{SWIR1 + NIR}$$
        
        Urban index
        """)


# ============================================================================
# 🗺️ PAGE 4: CLASSIFICATION
# ============================================================================

def page_classification():
    """Classification and prediction."""
    st.markdown("<h1>Land Cover Classification</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); font-size: 16px;'>Select model and run classification on uploaded satellite data</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.uploaded_bands:
        st.markdown("""
        <div class='card'>
            <h3 style='text-align: center;'>Missing Data</h3>
            <p style='text-align: center;'>Please upload satellite bands first in the Upload tab</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>Classification Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selection
        model_choice = st.selectbox(
            "Select ML Model:",
            ["Random Forest (Recommended)", "Support Vector Machine", "K-Nearest Neighbors"],
            help="Choose the classifier for optimal results"
        )
        
        st.markdown("""
        <div style='background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px; margin: 16px 0;'>
            <p style='margin: 0; font-weight: 600; margin-bottom: 8px;'>Processing Pipeline:</p>
            <ul style='margin: 0; padding-left: 20px; font-size: 14px;'>
            <li>Load and validate bands</li>
            <li>Apply radiometric calibration</li>
            <li>Extract 10 features</li>
            <li>Run """ + model_choice.split("(")[0].strip() + """ classifier</li>
            <li>Generate colored map</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Classification button
        if st.button("Execute Classification", key="classify_btn", use_container_width=True):
            with st.spinner("Processing... This may take a few minutes..."):
                st.progress(0.2, text="Loading bands...")
                st.progress(0.4, text="Calibrating data...")
                st.progress(0.6, text="Computing indices...")
                st.progress(0.8, text="Running classification...")
                st.progress(1.0, text="Generating map...")
            
            st.success("Classification complete!")
            st.session_state.predictions = "dummy"
            st.session_state.statistics = "dummy"
    
    with col2:
        st.markdown("""
        <div class='card card-success'>
            <h3 style='margin-top: 0;'>Job Info</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Model", model_choice.split("(")[0].strip())
        st.metric("Classes", "4")
        st.metric("Status", "Ready" if st.session_state.uploaded_bands else "Waiting")


# ============================================================================
# 📊 PAGE 5: RESULTS
# ============================================================================

def page_results():
    """Results visualization and statistics."""
    st.markdown("<h1>Results & Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); font-size: 16px;'>Classification results, statistics, and export options</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.predictions:
        st.markdown("""
        <div class='card'>
            <h3 style='text-align: center;'>No Data Available</h3>
            <p style='text-align: center;'>Execute classification first in the Classification tab to view results</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("<h2 style='margin-bottom: 16px;'>Classification Map</h2>", unsafe_allow_html=True)
        
        # Create dummy classification map
        classification_map = np.random.choice([0, 1, 2, 3], (500, 500))
        color_map = np.zeros((500, 500, 3), dtype=np.uint8)
        
        # Apply colors
        color_map[classification_map == 0] = config.COLOR_PALETTE['water']
        color_map[classification_map == 1] = config.COLOR_PALETTE['agriculture']
        color_map[classification_map == 2] = config.COLOR_PALETTE['urban']
        color_map[classification_map == 3] = config.COLOR_PALETTE['desert']
        
        st.image(color_map, use_column_width=True, caption="Land Cover Classification Results")
    
    with col2:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>Land Cover Legend</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for class_id, class_name in config.CLASS_NAMES.items():
            color_hex = config.HEX_COLORS[class_name]
            count = np.sum(classification_map == class_id)
            area_km2 = count * config.KM_CONVERSION
            percent = (count / classification_map.size) * 100
            
            st.markdown(f"""
            <div style="padding: 10px; margin: 8px 0; border-radius: 6px; 
                        border-left: 3px solid {color_hex}; 
                        background: #F9FAFB;">
                <b style='color: {color_hex};'>{class_name.capitalize()}</b><br>
                <span style='font-size: 12px; color: #6B7280;'>{percent:.1f}% • {area_km2:.2f} km²</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Statistics table
    st.markdown("<h2>Detailed Statistics</h2>", unsafe_allow_html=True)
    
    stats_data = []
    for class_id, class_name in config.CLASS_NAMES.items():
        count = np.sum(classification_map == class_id)
        area_km2 = count * config.KM_CONVERSION
        percent = (count / classification_map.size) * 100
        
        stats_data.append({
            "Category": class_name.capitalize(),
            "Pixels": f"{count:,}",
            "Area (km²)": f"{area_km2:.2f}",
            "Percentage": f"{percent:.2f}%",
            "Confidence": f"{np.random.randint(85, 99)}%"
        })
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
    
    st.divider()
    
    # Download buttons
    st.markdown("<h3>Export & Download</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.download_button(
            "Download Map (PNG)",
            data=b"placeholder_image_data",
            file_name="classification_map.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        csv_data = pd.DataFrame(stats_data).to_csv(index=False)
        st.download_button(
            "Download Statistics (CSV)",
            data=csv_data,
            file_name="area_statistics.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            "Download Report (JSON)",
            data=json.dumps({"status": "completed", "classes": 4}, indent=2),
            file_name="classification_report.json",
            mime="application/json",
            use_container_width=True
        )


# ============================================================================
# 🎯 MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    setup_page_config()
    
    # Initialize session state
    if 'uploaded_bands' not in st.session_state:
        st.session_state.uploaded_bands = {}
    if 'mtl_data' not in st.session_state:
        st.session_state.mtl_data = None
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("## Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select Page:",
            ["Home", "Upload", "Preview", "Classification", "Results"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Resources")
        st.markdown("""
        - [Landsat 8 Documentation](https://landsat.usgs.gov/)
        - [Spectral Indices Guide](https://eos.com/indicedb/)
        - [Project Overview](./COMPLETE_OVERVIEW.md)
        """)
        
        st.markdown("---")
        st.markdown("### Team Members")
        
        team_members = [
            "Karim Mustafa Dasouki",
            "Mohamed Abd El-Moneim Mohamed Rashad",
            "Mohsen Mohamed El-Sayed",
            "Karim Hesham Mansour",
            "Abd El-Rahman Medhat Imam",
            "Mohamed Alaa El-Din Karam El-Sham",
            "Hussam Hassan Mahmoud Abd El-Aziz"
        ]
        
        for member in team_members:
            st.markdown(f"""
            <div class='team-member'>
            👤 {member}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary); font-size: 12px; padding: 12px 0;'>
            <p style='margin: 4px 0;'><b>Remote Sensing</b></p>
            <p style='margin: 4px 0;'>Land Classification System</p>
            <p style='margin: 4px 0;'>May 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if page == "Home":
        page_home()
    elif page == "Upload":
        page_upload()
    elif page == "Preview":
        page_preview()
    elif page == "Classification":
        page_classification()
    elif page == "Results":
        page_results()


if __name__ == "__main__":
    main()
