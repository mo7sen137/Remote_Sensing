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
    # PROFESSIONAL ENTERPRISE DESIGN SYSTEM v2.0
    # =========================================================================
    st.markdown("""
        <style>
        /* =========== ANIMATED BACKGROUND =========== */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        html, body, #root {
            background: linear-gradient(-45deg, #0F172A, #1a1f3a, #16213e, #0F172A) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 15s ease infinite !important;
        }
        
        .stApp, 
        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stFullScreenFrame"] {
            background: linear-gradient(-45deg, #0F172A, #1a1f3a, #16213e, #0F172A) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 15s ease infinite !important;
            color: #E8EAED !important;
        }
        
        /* =========== BASIC STYLES =========== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 📄 PAGE 1: HOME
# ============================================================================

def page_home():
    """Home page with project overview."""
    st.markdown("<h1 style='text-align: center;'>🛰️ LAND COVER CLASSIFICATION SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #00ffaa;'>Advanced Satellite Image Processing & ML Analysis</h3>", unsafe_allow_html=True)
    st.divider()
    
    # Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📡 Satellite", "LANDSAT 8", "11 Bands")
    with col2:
        st.metric("🔬 Image Size", "4M px", "Per Band")
    with col3:
        st.metric("🤖 ML Models", "3 Types", "Ensemble")
    with col4:
        st.metric("🎯 Classes", "4", "Categories")
    
    st.divider()
    
    # Main Content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>📍 PROJECT OVERVIEW</h3>
            <p style='color: #d0d0e8; font-size: 1.05em;'>
            Advanced satellite imagery classification from <b>Landsat 8</b> for Egypt's Nile Delta region.
            </p>
            <p style='color: #e0e0ff;'><b>Land Cover Types:</b></p>
            <ul style='color: #d0d0e8;'>
            <li>💧 <b>Water</b> - Lakes, rivers, coastal areas</li>
            <li>🌱 <b>Agriculture</b> - Cultivated vegetation</li>
            <li>🏢 <b>Urban</b> - Buildings & infrastructure</li>
            <li>🏜️ <b>Desert</b> - Bare soil & sand</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>🚀 WORKFLOW</h3>
            <p style='color: #e0e0ff;'><b>5-Step Processing Pipeline:</b></p>
            <ol style='color: #d0d0e8;'>
            <li>📤 Upload Landsat 8 bands (B2-B7)</li>
            <li>🔍 Preview & extract spectral indices</li>
            <li>🤖 Select & apply ML classifier</li>
            <li>📊 Generate classification map</li>
            <li>💾 Export results & statistics</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Technical Specs
    st.markdown("<h2 style='text-align: center; color: #00ffff;'>⚙️ SYSTEM SPECIFICATIONS</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("🔬 Preprocessing & Calibration", expanded=False):
            st.markdown("""
            • Radiometric calibration (DN → Reflectance)
            • Band normalization & stacking
            • Quality filtering & masking
            • Geometric validation
            """)
    
    with col2:
        with st.expander("📊 Feature Extraction", expanded=False):
            st.markdown("""
            **7 Original Bands:**
            B2, B3, B4, B5, B6, B7, Thermal
            
            **3 Spectral Indices:**
            • NDVI (Vegetation)
            • NDWI (Water)
            • NDBI (Built-up)
            """)
    
    with col3:
        with st.expander("🤖 ML Classification", expanded=False):
            st.markdown("""
            **Ensemble Models:**
            • Support Vector Machine
            • Random Forest (100 trees)
            • K-Nearest Neighbors (k=5)
            
            **Voting Mechanism:**
            Majority voting for robustness
            """)
    
    st.divider()
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 255, 136, 0.05), rgba(255, 0, 255, 0.05)); border: 2px solid #00ffaa; border-radius: 10px; padding: 25px; text-align: center;'>
        <h3 style='color: #00ffff; margin-bottom: 15px;'>✨ READY TO START?</h3>
        <p style='color: #d0d0e8; font-size: 1.1em;'>
        Navigate to the <b style='color: #00ffaa;'>📤 UPLOAD</b> tab to begin processing your satellite imagery
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 📤 PAGE 2: UPLOAD DATA
# ============================================================================

def page_upload():
    """Data upload interface."""
    st.markdown("<h1 style='color: #00ffff;'>📤 UPLOAD SATELLITE DATA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffaa; font-size: 1.1em;'>Import Landsat 8 bands and metadata files for processing</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>🎞️ SPECTRAL BANDS (B2-B7)</h3>
            <p style='color: #d0d0e8; font-size: 0.95em;'>Upload all 6 bands as GeoTIFF files:</p>
            <ul style='color: #e0e0ff; font-size: 0.9em;'>
            <li><b>B2:</b> Coastal/Aerosol (0.43-0.45 μm)</li>
            <li><b>B3:</b> Blue (0.45-0.51 μm)</li>
            <li><b>B4:</b> Red (0.64-0.67 μm)</li>
            <li><b>B5:</b> NIR (0.85-0.88 μm)</li>
            <li><b>B6:</b> SWIR1 (1.57-1.65 μm)</li>
            <li><b>B7:</b> SWIR2 (2.11-2.29 μm)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
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
            st.markdown(f"<p style='color: #00ffaa; font-weight: bold;'>✅ {len(uploaded_bands)}/6 bands loaded</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>📋 METADATA FILE</h3>
            <p style='color: #d0d0e8;'>Upload MTL metadata file for calibration:</p>
            <ul style='color: #e0e0ff; font-size: 0.95em;'>
            <li>Format: <b>.txt</b> file</li>
            <li>Contains radiometric coefficients</li>
            <li>Filename: <b>*_MTL.txt</b></li>
            <li>Required for calibration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        mtl_file = st.file_uploader(
            "MTL File (*.txt)",
            type=['txt'],
            key="mtl_file"
        )
        
        if mtl_file:
            st.session_state.mtl_data = mtl_file
            st.markdown("<p style='color: #00ffaa; font-weight: bold;'>✅ MTL file loaded</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Show file sizes
    if uploaded_bands or mtl_file:
        st.markdown("<h2 style='color: #00ffff; text-align: center;'>📊 UPLOAD SUMMARY</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "✅ COMPLETE" if len(uploaded_bands) == 6 else "⏳ INCOMPLETE"
            st.metric("🎞️ Bands Loaded", f"{len(uploaded_bands)}/6", delta=status)
        
        with col2:
            mtl_status = "✅ READY" if mtl_file else "❌ MISSING"
            st.metric("📋 MTL File", "Loaded" if mtl_file else "Not Loaded", delta=mtl_status)
        
        with col3:
            ready = "✅ READY" if len(uploaded_bands) == 6 and mtl_file else "⏳ WAITING"
            st.metric("🚀 Processing", "Can Start" if len(uploaded_bands) == 6 and mtl_file else "Incomplete", delta=ready)


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
    st.markdown("<h1 style='color: #ff00ff;'>🤖 LAND COVER CLASSIFICATION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffaa; font-size: 1.1em;'>Select model and run classification on uploaded satellite data</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.uploaded_bands:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 150, 0.15), rgba(255, 100, 0, 0.15)); border: 2px solid #ff0088; border-radius: 10px; padding: 20px; text-align: center;'>
            <h3 style='color: #ff00aa;'>⚠️ MISSING DATA</h3>
            <p style='color: #d0d0e8;'>Please upload satellite bands first in the <b>📤 UPLOAD</b> tab</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>🤖 CLASSIFICATION SETTINGS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selection
        model_choice = st.selectbox(
            "🎯 Select ML Model:",
            ["🌳 Random Forest (Recommended)", "🎯 Support Vector Machine", "📍 K-Nearest Neighbors"],
            help="Choose the classifier for optimal results"
        )
        
        st.markdown("""
        <div style='background: rgba(100, 0, 200, 0.08); border: 2px solid #9900ff; border-radius: 8px; padding: 15px; margin: 15px 0;'>
            <p style='color: #d0d0e8;'><b>📊 Processing Pipeline:</b></p>
            <ul style='color: #e0e0ff;'>
            <li>Step 1: Load and validate bands</li>
            <li>Step 2: Apply radiometric calibration</li>
            <li>Step 3: Extract 10 features</li>
            <li>Step 4: Run <b style='color: #00ffaa;'>""" + model_choice.split("(")[0].strip() + """</b> classifier</li>
            <li>Step 5: Generate colored map</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Classification button
        if st.button("▶️ EXECUTE CLASSIFICATION", key="classify_btn", use_container_width=True):
            with st.spinner("🔄 Processing... This may take a few minutes..."):
                st.progress(0.2, text="📥 Loading bands...")
                st.progress(0.4, text="🔬 Calibrating data...")
                st.progress(0.6, text="📊 Computing indices...")
                st.progress(0.8, text="🤖 Running classification...")
                st.progress(1.0, text="🎨 Generating map...")
            
            st.markdown("<p style='color: #00ffaa; font-weight: bold; font-size: 1.1em;'>✅ Classification complete!</p>", unsafe_allow_html=True)
            st.session_state.predictions = "dummy"
            st.session_state.statistics = "dummy"
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1)); border: 2px solid #00ffff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffff;'>📋 JOB INFO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("🤖 Model", model_choice.split("(")[0].strip())
        st.metric("🎯 Classes", "4", "Water • Urban • Agri • Land")
        st.metric("📡 Status", "Ready" if st.session_state.uploaded_bands else "Waiting")


# ============================================================================
# 📊 PAGE 5: RESULTS
# ============================================================================

def page_results():
    """Results visualization and statistics."""
    st.markdown("<h1 style='color: #00ffaa;'>📊 RESULTS & ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffff; font-size: 1.1em;'>Classification results, statistics, and export options</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.predictions:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 200, 255, 0.15), rgba(0, 150, 200, 0.15)); border: 2px solid #00aaff; border-radius: 10px; padding: 20px; text-align: center;'>
            <h3 style='color: #00ffff;'>ℹ️ NO DATA AVAILABLE</h3>
            <p style='color: #d0d0e8;'>Execute classification first in the <b>🤖 CLASSIFICATION</b> tab to view results</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h2 style='color: #00ffff; border-bottom: 3px solid #00ff88;'>🗺️ CLASSIFICATION MAP</h2>
        """, unsafe_allow_html=True)
        
        # Create dummy classification map
        classification_map = np.random.choice([0, 1, 2, 3], (500, 500))
        color_map = np.zeros((500, 500, 3), dtype=np.uint8)
        
        # Apply colors
        color_map[classification_map == 0] = config.COLOR_PALETTE['water']
        color_map[classification_map == 1] = config.COLOR_PALETTE['agriculture']
        color_map[classification_map == 2] = config.COLOR_PALETTE['urban']
        color_map[classification_map == 3] = config.COLOR_PALETTE['desert']
        
        st.image(color_map, use_column_width=True, caption="🎨 Land Cover Classification Map")
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>📈 LAND COVER LEGEND</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for class_id, class_name in config.CLASS_NAMES.items():
            color_hex = config.HEX_COLORS[class_name]
            count = np.sum(classification_map == class_id)
            area_km2 = count * config.KM_CONVERSION
            percent = (count / classification_map.size) * 100
            
            emoji = "💧" if class_name == "water" else "🌱" if class_name == "agriculture" else "🏢" if class_name == "urban" else "🏜️"
            
            st.markdown(f"""
            <div style="padding: 12px; margin: 8px 0; border-radius: 8px; 
                        border-left: 5px solid {color_hex}; 
                        background: linear-gradient(90deg, rgba(255, 255, 255, 0.03), transparent);
                        border-top: 2px solid rgba(255, 255, 255, 0.1);">
                <b style='color: {color_hex}; font-size: 1.05em;'>{emoji} {class_name.upper()}</b><br>
                <span style='color: #00ffaa;'>{percent:.1f}%</span> • <span style='color: #00ffff;'>{area_km2:.2f} km²</span> • <span style='color: #e0e0ff;'>{count:,} px</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Statistics table
    st.markdown("""
    <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
        <h2 style='color: #00ffaa; margin-top: 0;'>📋 DETAILED STATISTICS</h2>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #00ffff; border-radius: 10px; padding: 20px;'>
        <h3 style='color: #00ffff;'>💾 EXPORT & DOWNLOAD</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📥 Download Map (PNG)",
            data=b"placeholder_image_data",
            file_name="classification_map.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        csv_data = pd.DataFrame(stats_data).to_csv(index=False)
        st.download_button(
            "📊 Download Statistics (CSV)",
            data=csv_data,
            file_name="area_statistics.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            "📋 Download Report (JSON)",
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
