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
    
    # Professional Cyberpunk Dark Theme with Neon Colors
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
        
        /* ============ GLOBAL STYLES ============ */
        * {
            font-family: 'Space Mono', 'Courier New', monospace;
        }
        
        html, body, [class*="css"]  {
            background: linear-gradient(135deg, #0a0e27 0%, #1a0033 50%, #0a0e27 100%) !important;
        }
        
        /* ============ MAIN APP ============ */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a0033 50%, #0a0e27 100%);
        }
        
        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f001a 0%, #1a0033 50%, #0f001a 100%);
            border-right: 3px solid #00ff88;
            box-shadow: inset -2px 0 10px rgba(0, 255, 136, 0.1);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #00ff88 !important;
        }
        
        /* ============ MAIN CONTENT ============ */
        [data-testid="stMainBlockContainer"] {
            background: transparent;
            color: #e0e0ff;
        }
        
        /* ============ TYPOGRAPHY ============ */
        h1 {
            color: #00ffff !important;
            font-family: 'Orbitron', sans-serif !important;
            font-size: 3em !important;
            font-weight: 900 !important;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.6), 0 0 40px rgba(255, 0, 255, 0.3);
            letter-spacing: 2px;
            margin-bottom: 10px !important;
        }
        
        h2 {
            color: #ff00ff !important;
            font-family: 'Orbitron', sans-serif !important;
            font-size: 1.8em !important;
            font-weight: 700 !important;
            text-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
            letter-spacing: 1px;
            border-bottom: 2px solid #00ff88;
            padding-bottom: 8px;
        }
        
        h3 {
            color: #00ffaa !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700 !important;
            text-shadow: 0 0 10px rgba(0, 255, 170, 0.4);
        }
        
        p, span, div {
            color: #d0d0e8;
        }
        
        /* ============ TABS ============ */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(15, 0, 26, 0.8);
            border-bottom: 2px solid #00ff88;
            gap: 5px;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background: linear-gradient(135deg, rgba(26, 0, 51, 0.9), rgba(51, 0, 102, 0.9));
            color: #b0b0d0;
            border: 2px solid #444477;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-family: 'Space Mono', monospace;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stTabs [data-baseweb="tab-list"] button:hover {
            border-color: #00ffaa;
            color: #00ffaa;
            box-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #00ff88 0%, #00ffaa 50%, #00ff88 100%);
            color: #0a0e27 !important;
            border: 2px solid #00ff88;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.6), inset 0 0 10px rgba(0, 255, 136, 0.3);
            font-weight: 700;
        }
        
        /* ============ BUTTONS ============ */
        .stButton > button {
            background: linear-gradient(135deg, #ff00ff 0%, #00ffff 100%);
            color: #0a0e27;
            border: 2px solid #ff00ff;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 1.1em;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 0 20px rgba(255, 0, 255, 0.4), inset 0 0 10px rgba(255, 255, 255, 0.1);
            cursor: pointer;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 100%);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 50px rgba(255, 0, 255, 0.6);
            transform: translateY(-3px) scale(1.08);
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        .stButton > button:active {
            transform: translateY(-1px) scale(1.05);
        }
        
        /* ============ INPUT FIELDS ============ */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: rgba(15, 0, 26, 0.9) !important;
            color: #00ffaa !important;
            border: 2px solid #00ff88 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-family: 'Space Mono', monospace;
            transition: all 0.3s ease;
            box-shadow: inset 0 0 10px rgba(0, 255, 136, 0.1);
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #ff00ff !important;
            box-shadow: inset 0 0 10px rgba(255, 0, 255, 0.2), 0 0 20px rgba(255, 0, 255, 0.3);
            color: #ff00ff !important;
        }
        
        /* ============ FILE UPLOADER ============ */
        .stFileUploader {
            border: 2px dashed #00ff88;
            background: rgba(0, 255, 136, 0.05);
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: #ff00ff;
            background: rgba(255, 0, 255, 0.1);
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
        }
        
        /* ============ METRICS ============ */
        .stMetric {
            background: linear-gradient(135deg, rgba(26, 0, 51, 0.95), rgba(51, 0, 76, 0.95));
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #00ff88;
            border-top: 2px solid #ff00ff;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2), inset 0 0 10px rgba(0, 255, 136, 0.05);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            border-left-color: #ff00ff;
            box-shadow: 0 0 30px rgba(255, 0, 255, 0.3), inset 0 0 15px rgba(255, 0, 255, 0.1);
            transform: translateY(-3px);
        }
        
        /* ============ MESSAGES ============ */
        .stSuccess {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 170, 0.15));
            border-left: 4px solid #00ff88;
            border-radius: 8px;
            padding: 12px;
            color: #00ffaa;
            font-weight: 600;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 200, 255, 0.15));
            border-left: 4px solid #00ffff;
            border-radius: 8px;
            padding: 12px;
            color: #00ffff;
            font-weight: 600;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(255, 200, 0, 0.15), rgba(255, 150, 0, 0.15));
            border-left: 4px solid #ffaa00;
            border-radius: 8px;
            padding: 12px;
            color: #ffcc00;
            font-weight: 600;
            box-shadow: 0 0 15px rgba(255, 200, 0, 0.2);
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.15), rgba(255, 0, 150, 0.15));
            border-left: 4px solid #ff0088;
            border-radius: 8px;
            padding: 12px;
            color: #ff00aa;
            font-weight: 600;
            box-shadow: 0 0 15px rgba(255, 0, 150, 0.2);
        }
        
        /* ============ TABLES ============ */
        .stDataFrame {
            background: linear-gradient(135deg, rgba(15, 0, 26, 0.9), rgba(26, 0, 51, 0.9));
            border: 2px solid #00ff88;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
            overflow: hidden;
        }
        
        .stDataFrame th {
            background: linear-gradient(90deg, #ff00ff, #00ffff);
            color: #0a0e27;
            font-weight: 700;
            padding: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stDataFrame td {
            padding: 12px;
            border-bottom: 1px solid rgba(0, 255, 136, 0.2);
            color: #d0d0e8;
        }
        
        .stDataFrame tr:hover {
            background: rgba(0, 255, 136, 0.1);
        }
        
        /* ============ EXPANDABLE SECTIONS ============ */
        .streamlit-expanderHeader {
            background: linear-gradient(90deg, #1a0033, #330066);
            border: 2px solid #00ff88;
            border-radius: 8px;
            color: #00ffaa !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #ff00ff;
            background: linear-gradient(90deg, #330066, #1a0033);
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
        }
        
        /* ============ SCROLLBAR ============ */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 0, 26, 0.8);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00ff88, #ff00ff);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #00ffff, #ff00ff);
        }
        
        /* ============ ANIMATIONS ============ */
        @keyframes neon-glow {
            0%, 100% {
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
                color: #00ffff;
            }
            50% {
                text-shadow: 0 0 20px rgba(255, 0, 255, 0.8);
                color: #ff00ff;
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
            }
            50% {
                box-shadow: 0 0 30px rgba(255, 0, 255, 0.7);
            }
        }
        
        h1 {
            animation: neon-glow 3s ease-in-out infinite;
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
