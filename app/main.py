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
    """Configure Streamlit page settings with Cyberpunk theme."""
    st.set_page_config(
        page_title="🛰️ Remote Sensing Land Classification",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark theme (Cyberpunk style)
    st.markdown("""
        <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        /* Main background */
        .stApp {
            background-color: #0a0e27 !important;
        }
        
        html, body {
            background-color: #0a0e27 !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1a1f3a !important;
            border-right: 2px solid #e94560;
        }
        
        /* Main content area */
        section[data-testid="stMainBlockContainer"] {
            background-color: #0a0e27 !important;
            color: #eaeaea !important;
        }
        
        .main {
            background-color: #0a0e27 !important;
            color: #eaeaea !important;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ff6b9d !important;
            font-weight: 700 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #1a1f3a;
            color: #eaeaea;
            border-radius: 5px;
            border: 1px solid #2d3748;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #e94560;
            color: white;
            border: 2px solid #ff6b9d;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #e94560;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #ff6b9d;
            transform: scale(1.05);
        }
        
        /* Input fields */
        input, .stTextInput, .stNumberInput {
            background-color: #1a1f3a !important;
            color: #eaeaea !important;
            border: 1px solid #2d3748 !important;
        }
        
        /* Cards */
        .stMetric {
            background-color: #1a1f3a;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e94560;
        }
        
        /* Success/Info messages */
        .stSuccess {
            background-color: rgba(76, 175, 80, 0.1);
        }
        
        .stInfo {
            background-color: rgba(33, 150, 243, 0.1);
        }
        
        .stWarning {
            background-color: rgba(255, 152, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 📄 PAGE 1: HOME
# ============================================================================

def page_home():
    """Home page with project overview."""
    st.markdown("# 🛰️ Remote Sensing Land Classification")
    st.markdown("### Automated Land Cover Mapping from Satellite Imagery")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## 📍 About This Project
        
        This application classifies satellite images into **4 land cover types**:
        - 💧 **Water** - Lakes, rivers, seas
        - 🌱 **Agriculture** - Crops and vegetation
        - 🏢 **Urban** - Buildings and infrastructure
        - 🏜️ **Desert** - Bare soil and sand
        
        **Using:** Landsat 8 satellite imagery from the Nile Delta region of Egypt.
        """)
    
    with col2:
        st.markdown("""
        ## 🎯 How It Works
        
        1. Upload Landsat 8 bands (B2-B7)
        2. Upload MTL metadata file
        3. Select a ML model (SVM, RF, KNN)
        4. Click "Classify" to process
        5. View results as:
           - 🗺️ Colored classification map
           - 📊 Area statistics
           - 📈 Distribution chart
        """)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Resolution", "30m", "Per pixel")
    with col2:
        st.metric("Image Size", "2000×2000", "Pixels")
    with col3:
        st.metric("Total Pixels", "4M", "Processed")
    with col4:
        st.metric("Classes", "4", "Categories")
    
    st.markdown("---")
    st.info("👉 Go to **Upload Data** tab to get started!")


# ============================================================================
# 📤 PAGE 2: UPLOAD DATA
# ============================================================================

def page_upload():
    """Data upload interface."""
    st.markdown("# 📤 Upload Landsat 8 Data")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 🎞️ Spectral Bands (B2-B7)")
        st.info("""
        Upload all 7 bands as GeoTIFF files:
        - B2: Coastal/Aerosol (0.43-0.45 μm)
        - B3: Blue (0.45-0.51 μm)
        - B4: Red (0.64-0.67 μm)
        - B5: NIR (0.85-0.88 μm)
        - B6: SWIR1 (1.57-1.65 μm)
        - B7: SWIR2 (2.11-2.29 μm)
        """)
        
        uploaded_bands = {}
        for band_num in range(2, 8):
            uploaded_file = st.file_uploader(
                f"Band {band_num} (*.tif)",
                type=['tif', 'tiff'],
                key=f"band_{band_num}"
            )
            if uploaded_file:
                uploaded_bands[band_num] = uploaded_file
        
        if uploaded_bands:
            st.session_state.uploaded_bands = uploaded_bands
            st.success(f"✅ {len(uploaded_bands)}/6 bands loaded")
    
    with col2:
        st.markdown("## 📋 Metadata File")
        st.info("""
        Upload the MTL metadata file that comes with Landsat 8 data:
        - Format: .txt
        - Contains radiometric calibration coefficients
        - Filename: *_MTL.txt
        """)
        
        mtl_file = st.file_uploader(
            "MTL File (*.txt)",
            type=['txt'],
            key="mtl_file"
        )
        
        if mtl_file:
            st.session_state.mtl_data = mtl_file
            st.success("✅ MTL file loaded")
    
    st.markdown("---")
    
    # Show file sizes
    if uploaded_bands or mtl_file:
        st.markdown("## 📊 Upload Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Bands", f"{len(uploaded_bands)}/6", 
                     delta=None if len(uploaded_bands) == 6 else "Missing")
        
        with col2:
            if mtl_file:
                st.metric("MTL File", "✅ Loaded")
            else:
                st.metric("MTL File", "❌ Missing")
        
        with col3:
            total_bands = len(uploaded_bands)
            st.metric("Ready", "✅ Yes" if total_bands == 6 and mtl_file else "⏳ Waiting")


# ============================================================================
# 🔍 PAGE 3: PREVIEW & ANALYSIS
# ============================================================================

def page_preview():
    """Data preview and spectral analysis."""
    st.markdown("# 🔍 Data Preview & Analysis")
    
    if not st.session_state.uploaded_bands:
        st.warning("⚠️ Please upload bands first in the 'Upload Data' tab")
        return
    
    st.markdown("## 📊 Band Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Available Bands")
        for band_num in st.session_state.uploaded_bands.keys():
            st.text(f"✅ Band {band_num}")
    
    with col2:
        st.markdown("### Spectral Indices")
        st.text("NDVI - Vegetation Index")
        st.text("NDWI - Water Index")
        st.text("NDBI - Urban Index")
    
    with col3:
        st.markdown("### Processing Steps")
        st.text("1️⃣ Radiometric Calibration")
        st.text("2️⃣ Indices Calculation")
        st.text("3️⃣ ML Classification")
    
    st.markdown("---")
    
    # Show formulas
    st.markdown("## 🧮 Spectral Indices Formulas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### NDVI (Vegetation)
        $$NDVI = \\frac{NIR - Red}{NIR + Red}$$
        
        Shows vegetation areas in **green** ✅
        """)
    
    with col2:
        st.markdown("""
        ### NDWI (Water)
        $$NDWI = \\frac{NIR - SWIR1}{NIR + SWIR1}$$
        
        Shows water bodies in **blue** ✅
        """)
    
    with col3:
        st.markdown("""
        ### NDBI (Urban)
        $$NDBI = \\frac{SWIR1 - NIR}{SWIR1 + NIR}$$
        
        Shows urban areas in **red** ✅
        """)


# ============================================================================
# 🗺️ PAGE 4: CLASSIFICATION
# ============================================================================

def page_classification():
    """Classification and prediction."""
    st.markdown("# 🗺️ Land Cover Classification")
    
    if not st.session_state.uploaded_bands:
        st.warning("⚠️ Please upload bands first")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🤖 Classification Settings")
        
        # Model selection
        model_choice = st.selectbox(
            "Select ML Model:",
            ["Random Forest", "SVM", "KNN"],
            help="Choose the classifier to use"
        )
        
        # Classification button
        if st.button("▶️ Run Classification", key="classify_btn", use_container_width=True):
            with st.spinner("🔄 Processing... This may take a few minutes..."):
                st.progress(0.2, text="Loading bands...")
                st.progress(0.4, text="Calibrating data...")
                st.progress(0.6, text="Computing indices...")
                st.progress(0.8, text="Running classification...")
                st.progress(1.0, text="Generating map...")
            
            st.success("✅ Classification complete!")
            st.session_state.predictions = "dummy"  # Placeholder
            st.session_state.statistics = "dummy"   # Placeholder
    
    with col2:
        st.markdown("## 📋 Classification Info")
        
        st.metric("Model", model_choice)
        st.metric("Classes", "4")
        st.metric("Status", "Ready" if st.session_state.uploaded_bands else "Waiting")


# ============================================================================
# 📊 PAGE 5: RESULTS
# ============================================================================

def page_results():
    """Results visualization and statistics."""
    st.markdown("# 📊 Results & Statistics")
    
    if not st.session_state.predictions:
        st.info("ℹ️ Run classification first to see results")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🗺️ Classification Map")
        
        # Create dummy classification map
        classification_map = np.random.choice([0, 1, 2, 3], (500, 500))
        color_map = np.zeros((500, 500, 3), dtype=np.uint8)
        
        # Apply colors
        color_map[classification_map == 0] = config.COLOR_PALETTE['water']
        color_map[classification_map == 1] = config.COLOR_PALETTE['agriculture']
        color_map[classification_map == 2] = config.COLOR_PALETTE['urban']
        color_map[classification_map == 3] = config.COLOR_PALETTE['desert']
        
        st.image(color_map, use_column_width=True, caption="Classified Land Cover Map")
    
    with col2:
        st.markdown("## 📈 Legend")
        
        for class_id, class_name in config.CLASS_NAMES.items():
            color_hex = config.HEX_COLORS[class_name]
            count = np.sum(classification_map == class_id)
            area_km2 = count * config.KM_CONVERSION
            percent = (count / classification_map.size) * 100
            
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; border-radius: 5px; 
                        border-left: 4px solid {color_hex}; background-color: #1a1f3a;">
                <b>{class_name.upper()}</b> ({percent:.1f}%)<br>
                {area_km2:.2f} km² | {count:,} pixels
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics table
    st.markdown("## 📋 Detailed Statistics")
    
    stats_data = []
    for class_id, class_name in config.CLASS_NAMES.items():
        count = np.sum(classification_map == class_id)
        area_km2 = count * config.KM_CONVERSION
        percent = (count / classification_map.size) * 100
        
        stats_data.append({
            "Land Cover Type": class_name.capitalize(),
            "Pixel Count": f"{count:,}",
            "Area (km²)": f"{area_km2:.2f}",
            "Percentage (%)": f"{percent:.2f}"
        })
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
    
    # Download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📥 Download Map (PNG)",
            data=b"placeholder_image_data",
            file_name="classification_map.png",
            mime="image/png"
        )
    
    with col2:
        csv_data = pd.DataFrame(stats_data).to_csv(index=False)
        st.download_button(
            "📊 Download Statistics (CSV)",
            data=csv_data,
            file_name="area_statistics.csv",
            mime="text/csv"
        )
    
    with col3:
        st.download_button(
            "📋 Download Report (JSON)",
            data=json.dumps({"status": "completed", "classes": 4}),
            file_name="classification_report.json",
            mime="application/json"
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
        st.markdown("# ⚙️ Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select Page:",
            ["🏠 Home", "📤 Upload Data", "🔍 Preview", "🗺️ Classification", "📊 Results"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Landsat 8 Info](https://landsat.usgs.gov/)
        - [NDVI Guide](https://eos.com/indicedb/)
        - [Project Guide](./COMPLETE_OVERVIEW.md)
        """)
        
        st.markdown("---")
        st.markdown("### 👥 Team")
        st.text("Remote Sensing Project")
        st.text("May 2026")
    
    # Main content
    if page == "🏠 Home":
        page_home()
    elif page == "📤 Upload Data":
        page_upload()
    elif page == "🔍 Preview":
        page_preview()
    elif page == "🗺️ Classification":
        page_classification()
    elif page == "📊 Results":
        page_results()


if __name__ == "__main__":
    main()
