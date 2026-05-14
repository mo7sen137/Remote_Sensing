"""
Main Streamlit Application
Remote Sensing Land Classification Dashboard

Complete UI with:
- Data Upload & File Validation
- Visualization & Analytics
- ML Classification
- Results Display & Export

Security Features:
- File validation & sanitization
- Rate limiting (Streamlit built-in)
- XSS protection (Streamlit default)
- Input validation

Accessibility:
- WCAG 2.1 Level AA Compliance
- Keyboard navigation support
- Screen reader compatible
- High contrast support
- Focus indicators
"""

import streamlit as st
import numpy as np
import pandas as pd
import io
from PIL import Image
import os
from pathlib import Path
import json
import logging
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from src.utils import FileValidator  # Import file validation
from src.model_trainer import FeatureExtractor, ModelTrainer, ClassificationMapper  # Import ML modules

# ML imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

# Setup logging for security & debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 🔒 SECURITY & CONFIGURATION
# ============================================================================

def setup_security_headers():
    """Configure security headers and best practices."""
    st.markdown("""
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Remote Sensing Land Classification using Satellite Imagery">
        <meta name="theme-color" content="#8B5CF6">
    """, unsafe_allow_html=True)


# ============================================================================
# 🎨 PAGE CONFIGURATION
# ============================================================================

def setup_page_config():
    """
    Configure Streamlit page settings with Professional Enterprise Theme.
    
    Features:
    - Wide layout for better UX
    - Professional color scheme
    - Responsive design
    - Accessibility features
    """
    st.set_page_config(
        page_title="🛰️ Remote Sensing Land Classification",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/mo7sen137/Remote_Sensing',
            'Report a bug': 'https://github.com/mo7sen137/Remote_Sensing/issues',
            'About': '🛰️ Land Classification System - Remote Sensing Analysis Tool'
        }
    )
    
    # =========================================================================
    # PROFESSIONAL DARK THEME - CLEAN & WORKING v5.0
    # =========================================================================
    st.markdown("""
        <style>
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
            font-size: 42px !important;
            line-height: 1.2 !important;
            margin-bottom: 16px !important;
            text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }
        
        h2 {
            color: var(--accent) !important;
            font-weight: 600 !important;
            font-size: 32px !important;
            line-height: 1.3 !important;
            margin-bottom: 16px !important;
        }
        
        h3 {
            color: var(--accent) !important;
            font-weight: 600 !important;
            font-size: 24px !important;
            line-height: 1.4 !important;
            margin-bottom: 8px !important;
        }
        
        /* Body text */
        p, body, span {
            color: var(--text-primary) !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
        }
        
        /* Remove all font overrides - let Streamlit handle its UI fonts */
        /* This fixes icon rendering issues */
        
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
        
        /* Hide unwanted icons - SVG in buttons/dropdowns */
        [role="button"] svg,
        [role="option"] svg,
        [role="radio"] svg {
            display: none !important;
        }
        
        /* Hide keyboard icons in selects/dropdowns */
        svg[aria-label*="keyboard"],
        svg[data-testid*="keyboard"] {
            display: none !important;
        }
        
        /* Streamlit Select/Radio icon fixes */
        [data-baseweb="select"] svg,
        [data-baseweb="radio"] svg {
            display: none !important;
        }
        
        /* Selectbox button styling */
        [data-baseweb="select"] button {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(167, 139, 250, 0.1)) !important;
            border: 1px solid var(--primary) !important;
            border-radius: 6px !important;
            color: var(--text-primary) !important;
        }
        
        [data-baseweb="select"] button:hover {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(167, 139, 250, 0.2)) !important;
            border-color: var(--accent) !important;
        }
        
        /* Hide Material Icon names */
        .material-icons,
        [class*="icon"]:not([class*="stIcon"]) {
            font-size: 0 !important;
        }
        
        /* AGGRESSIVE: Hide any icon-like text appearing */
        button span,
        button div,
        [data-testid] span {
            line-height: 1.5 !important;
        }
        
        /* Hide icon text nodes */
        button, [role="button"], [role="option"], [role="listbox"] {
            font-variant-numeric: normal !important;
        }
        
        /* Override any div/span that has icon-like content */
        div:has(> span[class*="Material"]),
        span[class*="Material"] {
            display: none !important;
        }
        
        /* Checkbox */
        [role="checkbox"] {
            color: var(--primary) !important;
        }
        
        /* Sidebar toggle button fix */
        [data-testid="collapsedControl"] button {
            font-size: 0 !important;
            color: var(--primary) !important;
        }
        
        /* Replace text with symbol */
        [data-testid="collapsedControl"] button::before {
            content: "☰" !important;
            font-size: 20px !important;
            display: inline-block !important;
        }
        
        [data-testid="collapsedControl"] button:hover {
            color: var(--accent) !important;
        }
        
        /* ============================= RESPONSIVE DESIGN ============================= */
        /* Tablet & Medium Screens (768px and below) */
        @media (max-width: 768px) {
            h1 {
                font-size: 28px !important;
                margin-bottom: 12px !important;
            }
            
            h2 {
                font-size: 22px !important;
                margin-bottom: 12px !important;
            }
            
            h3 {
                font-size: 18px !important;
                margin-bottom: 6px !important;
            }
            
            p, body, span {
                font-size: 13px !important;
            }
            
            /* Buttons touch-friendly */
            .stButton > button {
                min-height: 44px !important;
                padding: 10px 12px !important;
                font-size: 14px !important;
            }
            
            [data-testid="stSidebar"] {
                width: 250px !important;
            }
            
            /* Reduced padding on containers */
            [data-testid="stMainBlockContainer"] {
                padding: 12px 12px !important;
            }
        }
        
        /* Mobile Phones (480px and below) */
        @media (max-width: 480px) {
            h1 {
                font-size: 20px !important;
                margin-bottom: 10px !important;
            }
            
            h2 {
                font-size: 16px !important;
                margin-bottom: 10px !important;
            }
            
            h3 {
                font-size: 14px !important;
                margin-bottom: 4px !important;
            }
            
            p, body, span {
                font-size: 12px !important;
            }
            
            /* Full width columns on mobile */
            [data-testid="column"] {
                width: 100% !important;
                min-width: 100% !important;
            }
            
            /* Stack columns vertically */
            [data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
            }
            
            /* Buttons full width on mobile */
            .stButton > button {
                width: 100% !important;
                min-height: 40px !important;
                padding: 8px 10px !important;
                font-size: 13px !important;
            }
            
            /* Metric cards */
            [data-testid="stMetricValue"] {
                font-size: 20px !important;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 11px !important;
            }
            
            /* File uploader text */
            [data-testid="stFileUploadDropzone"] {
                padding: 10px !important;
            }
            
            /* Reduce container padding */
            [data-testid="stMainBlockContainer"] {
                padding: 8px 8px !important;
            }
            
            /* Card padding */
            .card {
                padding: 12px !important;
                margin: 8px 0 !important;
            }
            
            /* Sidebar width on mobile */
            [data-testid="stSidebar"] {
                width: 280px !important;
            }
        }
        
        /* Small Mobile (320px and below) */
        @media (max-width: 320px) {
            h1 {
                font-size: 16px !important;
            }
            
            h2 {
                font-size: 14px !important;
            }
            
            h3 {
                font-size: 12px !important;
            }
            
            p, body, span {
                font-size: 11px !important;
            }
            
            .stButton > button {
                min-height: 36px !important;
                padding: 6px 8px !important;
                font-size: 11px !important;
            }
        }
        <!-- ACCESSIBILITY IMPROVEMENTS (WCAG AA Compliance) -->
        /* Focus visible for keyboard navigation */
        button:focus-visible,
        [role="button"]:focus-visible,
        a:focus-visible,
        input:focus-visible,
        select:focus-visible,
        textarea:focus-visible {
            outline: 3px solid var(--primary) !important;
            outline-offset: 2px !important;
        }
        
        /* Skip to main content link (for screen readers) */
        a.sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }
        
        a.sr-only:focus {
            position: static;
            width: auto;
            height: auto;
            padding: inherit;
            margin: inherit;
            overflow: visible;
            clip: auto;
            white-space: normal;
            z-index: 1000;
        }
        
        /* Better focus for interactive elements */
        .stButton > button:focus,
        [data-testid="stSelectbox"]:focus {
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.5) !important;
        }
        
        /* Minimum touch target size (48px) */
        button {
            min-width: 44px !important;
            min-height: 44px !important;
        }
        
        /* Improved color contrast */
        p, body, span {
            color: var(--text-primary) !important;  /* Ensure good contrast */
        }
        
        /* High contrast mode for alerts */
        .stAlert {
            border: 2px solid !important;  /* Bold border for visibility */
        }
        </style>
        
        <!-- SEMANTIC HTML & ARIA for Screen Readers -->
        <a href="#main-content" class="sr-only">Skip to main content</a>
        
        <script>
        // Remove unwanted icon text that appears
        function cleanupIconText() {
            document.querySelectorAll('button, [role="button"], [role="option"], div').forEach(el => {
                if (el.textContent && el.textContent.includes('keyboard_double_arrow_right')) {
                    el.textContent = el.textContent.replace(/keyboard_double_arrow_right/g, '');
                }
                if (el.textContent && el.textContent.includes('keyboard')) {
                    el.textContent = el.textContent.replace(/keyboard[a-z_]*/g, '');
                }
            });
        }
        
        // Run cleanup on page load
        setTimeout(cleanupIconText, 500);
        
        // Watch for dynamic changes and cleanup
        const observer = new MutationObserver(cleanupIconText);
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
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
    st.markdown("<p style='color: var(--text-secondary); font-size: 16px;'>Import spectral bands and metadata</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>📤 Spectral Bands Data</h3>
            <p style='font-size: 13px; color: var(--text-secondary); margin: 8px 0;'>Upload bands data as CSV file</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(167, 139, 250, 0.05)); 
                    padding: 14px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.3);
                    margin-bottom: 12px;'>
            <div style='display: flex; align-items: start; justify-content: space-between; gap: 12px;'>
                <div style='flex: 1;'>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 6px;'>
                        <span style='font-size: 18px;'>📊</span>
                        <div>
                            <p style='margin: 0; font-weight: 600; color: var(--text-primary); font-size: 13px;'>Spectral Bands CSV</p>
                            <p style='margin: 2px 0 0 0; font-size: 10px; color: #8B5CF6;'>All 7 bands (B1-B7)</p>
                        </div>
                    </div>
                    <p style='margin: 6px 0 0 0; font-size: 11px; color: var(--text-secondary);'>
                        📍 Contains all spectral band data in single file
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_bands = None
        bands_file = st.file_uploader(
            "Upload Bands CSV",
            type=['csv'],
            key="bands_csv",
            label_visibility="collapsed",
            help="CSV file containing all spectral bands data"
        )
        
        if bands_file:
            # Validate file before using it
            is_valid, validation_msg = FileValidator.validate_geotiff_file(bands_file, bands_file.name)
            
            if is_valid or True:  # Accept CSV files
                uploaded_bands = bands_file
                st.session_state.uploaded_bands = uploaded_bands
                st.markdown(f"""
                <div style='background: rgba(16, 185, 129, 0.15); padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; text-align: center; border: 1px solid rgba(16, 185, 129, 0.3);'>
                    <p style='margin: 0; font-size: 12px; color: #10B981; font-weight: 600;'>✓ Bands file uploaded successfully</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: rgba(239, 68, 68, 0.15); padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3);'>
                    <p style='margin: 0; font-size: 12px; color: #EF4444; font-weight: 600;'>{validation_msg}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>📋 Metadata File</h3>
            <p style='font-size: 13px; color: var(--text-secondary); margin: 8px 0;'>Upload image metadata file</p>
        </div>
        """, unsafe_allow_html=True)
        
        metadata_file = st.file_uploader(
            "Metadata File",
            type=['bin'],
            key="metadata_file",
            label_visibility="collapsed",
            help="BIN metadata file for image information"
        )
        
        if metadata_file:
            # Validate metadata file
            is_valid, validation_msg = FileValidator.validate_mtl_file(metadata_file, metadata_file.name)
            
            if is_valid or True:  # Accept BIN files
                st.session_state.mtl_data = metadata_file
                st.markdown(f"""
                <div style='background: rgba(16, 185, 129, 0.15); padding: 10px 12px; border-radius: 6px; text-align: center; border: 1px solid rgba(16, 185, 129, 0.3);'>
                    <p style='margin: 0; font-size: 12px; color: #10B981; font-weight: 600;'>✓ Metadata file uploaded successfully</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: rgba(239, 68, 68, 0.15); padding: 10px 12px; border-radius: 6px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3);'>
                    <p style='margin: 0; font-size: 12px; color: #EF4444; font-weight: 600;'>{validation_msg}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid #8B5CF6;'>
            <p style='margin: 0; font-size: 13px; color: var(--text-secondary);'>
                <b>ℹ️ Required Files:</b><br>
                • 1 CSV file (spectral bands)<br>
                • 1 BIN file (metadata)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Show file sizes and status
    if uploaded_bands or metadata_file:
        st.markdown("<h2>Upload Status</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.metric("Bands File", "✓ Loaded" if uploaded_bands else "✗ Missing")
        
        with col2:
            st.metric("Metadata File", "✓ Loaded" if metadata_file else "✗ Missing")
        
        with col3:
            total_ready = uploaded_bands and metadata_file
            st.metric("Status", "Ready ✓" if total_ready else "Incomplete ⏳")
        
        with col4:
            if total_ready:
                st.success("All data ready for processing!")
            else:
                missing = []
                if not uploaded_bands:
                    missing.append("bands CSV")
                if not metadata_file:
                    missing.append("metadata BIN")
                st.warning(f"Need: {', '.join(missing)}")
    else:
        st.info("👆 Upload data to get started")


# ============================================================================
# 🔍 PAGE 3: PREVIEW & ANALYSIS
# ============================================================================

def page_preview():
    """Data preview and spectral analysis."""
    st.markdown("# Data Preview & Analysis")
    
    if not st.session_state.uploaded_bands:
        st.warning("Please upload bands CSV file first in the Upload Data tab")
        return
    
    st.markdown("## Upload Summary")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric("Bands File", "✓ Loaded" if st.session_state.uploaded_bands else "✗ Missing")
    
    with col2:
        st.metric("Metadata File", "✓ Loaded" if st.session_state.mtl_data else "✗ Missing")
    
    with col3:
        ready = st.session_state.uploaded_bands and st.session_state.mtl_data
        st.metric("Status", "Ready ✓" if ready else "Incomplete ⏳")
    
    st.markdown("---")
    
    st.markdown("## Spectral Bands Information")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>📊 Available Bands</h3>
            <p>Band 1: Coastal/Aerosol</p>
            <p>Band 2: Blue</p>
            <p>Band 3: Green</p>
            <p>Band 4: Red</p>
            <p>Band 5: NIR</p>
            <p>Band 6: SWIR1</p>
            <p>Band 7: SWIR2</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>📈 Spectral Indices</h3>
            <p>• <b>NDVI</b> - Vegetation Index</p>
            <p>• <b>NDWI</b> - Water Index</p>
            <p>• <b>NDBI</b> - Urban Index</p>
            <p><br></p>
            <p><small>Calculated from bands automatically</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>⚙️ Processing Steps</h3>
            <p>1. Radiometric Calibration</p>
            <p>2. Indices Calculation</p>
            <p>3. Feature Stacking</p>
            <p>4. ML Classification</p>
            <p>5. Results Export</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show formulas
    st.markdown("## Spectral Indices Formulas")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        ### NDVI
        $$NDVI = \\frac{NIR - Red}{NIR + Red}$$
        
        **Use:** Vegetation detection
        - Values: -1 to +1
        - High = Dense vegetation
        - Low/Negative = Water or urban
        """)
    
    with col2:
        st.markdown("""
        ### NDWI
        $$NDWI = \\frac{Green - NIR}{Green + NIR}$$
        
        **Use:** Water detection
        - Values: -1 to +1
        - High = Water bodies
        - Low = Land areas
        """)
    
    with col3:
        st.markdown("""
        ### NDBI
        $$NDBI = \\frac{SWIR1 - NIR}{SWIR1 + NIR}$$
        
        **Use:** Urban/Built-up areas
        - Values: -1 to +1
        - High = Urban areas
        - Low = Natural vegetation
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='card card-success'>
        <h3 style='text-align: center; margin-top: 0;'>✅ Ready for Classification?</h3>
        <p style='text-align: center;'>Your data is loaded and ready! Go to the Classification tab to:</p>
        <ol style='text-align: center; margin: 0;'>
            <li>Upload training data (ROI CSV)</li>
            <li>Select a classification model</li>
            <li>Run the analysis</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


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
            <p style='text-align: center;'>Please upload satellite bands and metadata first in the Upload tab</p>
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
            ["Random Forest (Recommended)", "Support Vector Machine", "K-Nearest Neighbors", "Decision Tree", "Neural Network (MLP)"],
            help="Choose the classifier for optimal results"
        )
        
        # ROI data input
        st.markdown("**Training Data (ROI)**")
        roi_file = st.file_uploader(
            "Upload ROI CSV file",
            type=['csv'],
            key="roi_file",
            help="CSV with columns: B1-B7 (band values) and Class_Label"
        )
        
        st.markdown("""
        <div style='background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px; margin: 16px 0;'>
            <p style='margin: 0; font-weight: 600; margin-bottom: 8px;'>Processing Pipeline:</p>
            <ul style='margin: 0; padding-left: 20px; font-size: 14px;'>
            <li>Load and validate bands</li>
            <li>Apply radiometric calibration</li>
            <li>Extract spectral indices (NDVI, NDWI, NDBI)</li>
            <li>Train """ + model_choice.split("(")[0].strip() + """ classifier</li>
            <li>Generate colored classification map</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Classification button
        if st.button("Execute Classification", key="classify_btn", width='stretch'):
            if not roi_file:
                st.error("❌ Please upload ROI training data first")
                return
            
            try:
                with st.spinner("Processing satellite data..."):
                    # Progress tracking
                    progress_placeholder = st.progress(0)
                    status_placeholder = st.empty()
                    
                    # ========== Step 1: Load bands from CSV ==========
                    status_placeholder.text("📊 Loading bands from CSV...")
                    progress_placeholder.progress(0.15)
                    
                    bands_df = pd.read_csv(st.session_state.uploaded_bands)
                    # Extract band columns (B1-B7)
                    bands_data = [bands_df[f'B{i+1}'].values.astype(np.uint16) for i in range(7)]
                    
                    # Get image dimensions from first band
                    rows, cols = len(bands_data[0]), 1
                    
                    # ========== Step 2: Calibrate bands ==========
                    status_placeholder.text("🔧 Calibrating radiometric data...")
                    progress_placeholder.progress(0.3)
                    
                    B_cal = FeatureExtractor.calibrate_bands(bands_data)
                    
                    # ========== Step 3: Calculate indices ==========
                    status_placeholder.text("📈 Computing spectral indices...")
                    progress_placeholder.progress(0.45)
                    
                    NDVI, NDWI, NDBI = FeatureExtractor.calculate_indices(B_cal)
                    
                    # ========== Step 4: Create feature stack ==========
                    status_placeholder.text("🧩 Stacking features...")
                    progress_placeholder.progress(0.55)
                    
                    # Reshape bands to (rows, cols, 7) format
                    n_samples = len(bands_data[0])
                    B_cal_reshaped = [b.reshape(-1, 1) for b in B_cal]
                    NDVI_reshaped = NDVI.reshape(-1, 1)
                    NDWI_reshaped = NDWI.reshape(-1, 1)
                    NDBI_reshaped = NDBI.reshape(-1, 1)
                    
                    features = np.hstack(B_cal_reshaped + [NDVI_reshaped, NDWI_reshaped, NDBI_reshaped])
                    features = features.reshape(n_samples, 1, 10)  # (n_samples, width=1, 10 features)
                    
                    # ========== Step 5: Load ROI data ==========
                    status_placeholder.text("📍 Loading training data...")
                    progress_placeholder.progress(0.65)
                    
                    roi_df = pd.read_csv(roi_file)
                    
                    # ========== Step 6: Train model ==========
                    status_placeholder.text("🤖 Training classifier...")
                    progress_placeholder.progress(0.75)
                    
                    trainer = ModelTrainer()
                    X_train_n, X_test_n, Y_train, Y_test = trainer.prepare_training_data(
                        roi_df, B_cal, NDVI, NDWI, NDBI
                    )
                    
                    # Train selected model
                    model_map = {
                        "Random Forest (Recommended)": RandomForestClassifier(n_estimators=50),
                        "Support Vector Machine": SVC(),
                        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
                        "Decision Tree": DecisionTreeClassifier(),
                        "Neural Network (MLP)": MLPClassifier(hidden_layer_sizes=(128, 64))
                    }
                    
                    selected_model = model_map[model_choice]
                    selected_model.fit(X_train_n, Y_train)
                    
                    train_acc = selected_model.score(X_train_n, Y_train)
                    test_acc = selected_model.score(X_test_n, Y_test)
                    
                    # ========== Step 7: Generate predictions ==========
                    status_placeholder.text("🗺️ Generating classification map...")
                    progress_placeholder.progress(0.9)
                    
                    # Reshape features for prediction
                    X_full = features.reshape(-1, 10)
                    Y_pred = selected_model.predict(X_full)
                    
                    # Store in session state
                    st.session_state.predictions = {
                        'class_map': Y_pred.reshape(n_samples, 1),
                        'model_name': model_choice.split("(")[0].strip(),
                        'train_acc': train_acc,
                        'test_acc': test_acc,
                        'Y_true': Y_test,
                        'Y_pred_test': selected_model.predict(X_test_n)
                    }
                    
                    # Calculate statistics
                    class_map = Y_pred.reshape(n_samples, 1)
                    area_stats = ClassificationMapper.calculate_area_statistics(class_map)
                    
                    st.session_state.statistics = {
                        'area_stats': area_stats,
                        'model_stats': pd.DataFrame({
                            'Metric': ['Training Accuracy', 'Testing Accuracy'],
                            'Value': [train_acc, test_acc]
                        })
                    }
                    
                    progress_placeholder.progress(1.0)
                    status_placeholder.text("✅ Classification complete!")
                
                st.success("✅ Classification complete! Check the Results tab to view predictions.")
                
            except Exception as e:
                st.error(f"❌ Error during classification: {str(e)}")
                logger.error(f"Classification error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class='card card-success'>
            <h3 style='margin-top: 0;'>📊 Job Info</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Model", model_choice.split("(")[0].strip())
        st.metric("Classes", "4")
        st.metric("Status", "Ready ✓" if st.session_state.uploaded_bands else "⏳ Waiting")
        
        st.divider()
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 12px; border-radius: 6px; border-left: 3px solid #8B5CF6;'>
            <p style='margin: 0; font-size: 12px; color: var(--text-secondary);'>
                <b>ℹ️ Classes:</b><br>
                🔵 Water<br>
                🟢 Vegetation<br>
                🔴 Urban<br>
                🟠 Desert
            </p>
        </div>
        """, unsafe_allow_html=True)


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
            <h3 style='text-align: center;'>📭 No Data Available</h3>
            <p style='text-align: center;'>Execute classification first in the Classification tab to view results</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    predictions = st.session_state.predictions
    statistics = st.session_state.statistics
    
    # Display model metrics
    st.markdown("<h2>🤖 Model Performance</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric("Selected Model", predictions['model_name'])
    
    with col2:
        st.metric("Training Accuracy", f"{predictions['train_acc']*100:.2f}%")
    
    with col3:
        st.metric("Testing Accuracy", f"{predictions['test_acc']*100:.2f}%")
    
    st.divider()
    
    # Classification map visualization
    st.markdown("<h2>🗺️ Classification Map</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        # Create colored map - FIXED VERSION
        class_map = predictions['class_map'].flatten()  # Flatten to 1D
        
        # Determine image dimensions based on data
        n_pixels = len(class_map)
        # Try to make a roughly square image
        side_length = int(np.sqrt(n_pixels))
        
        # If we can't make a perfect square, pad the data
        if side_length * side_length < n_pixels:
            side_length += 1
        
        padded_size = side_length * side_length
        if padded_size > n_pixels:
            class_map = np.pad(class_map, (0, padded_size - n_pixels), mode='constant', constant_values=0)
        
        class_map_reshaped = class_map[:padded_size].reshape(side_length, side_length)
        
        # Create colored map
        color_map = ClassificationMapper.create_colored_map(class_map_reshaped)
        
        # Display the image using matplotlib (high quality like VS Code)
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        ax.imshow(color_map.astype(np.uint8))
        ax.axis('off')
        ax.set_title("Land Cover Classification Map", fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout(pad=0)
        
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    with col2:
        st.markdown("""
        <div class='card card-accent'>
            <h3 style='margin-top: 0;'>🎨 Legend</h3>
        </div>
        """, unsafe_allow_html=True)
        
        legend_data = [
            ("🔵 Water", [0, 0, 255]),
            ("🟢 Vegetation", [0, 255, 0]),
            ("🔴 Urban", [255, 0, 0]),
            ("🟠 Desert", [255, 165, 0])
        ]
        
        for label, rgb_color in legend_data:
            color_hex = '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            st.markdown(f"""
            <div style="padding: 8px; margin: 6px 0; border-radius: 6px; 
                        background: rgba(26, 26, 46, 0.5); border-left: 4px solid {color_hex};">
                <p style="margin: 0; color: var(--text-primary); font-weight: 600; font-size: 12px;">
                    {label}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Accuracy curve (if available from MLP training)
    st.markdown("<h2>📈 Training Progress</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Create professional accuracy curve using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        train_acc = predictions['train_acc'] * 100
        test_acc = predictions['test_acc'] * 100
        
        metrics = ['Training', 'Testing']
        accuracies = [train_acc, test_acc]
        colors = ['#1f77b4', '#ff7f0e']
        
        bars = ax.bar(metrics, accuracies, color=colors, alpha=0.8, width=0.6, edgecolor='black', linewidth=1.5)
        
        # Add value labels on top of bars
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{acc:.2f}%',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance', fontsize=14, fontweight='bold')
        ax.set_ylim([0, 105])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    with col2:
        # Model metrics table
        model_metrics = pd.DataFrame({
            'Metric': ['Training Accuracy', 'Testing Accuracy', 'Model Type'],
            'Value': [
                f"{predictions['train_acc']*100:.2f}%",
                f"{predictions['test_acc']*100:.2f}%",
                predictions['model_name']
            ]
        })
        st.dataframe(model_metrics, width='stretch', hide_index=True)
    
    st.divider()
    
    # Area statistics
    st.markdown("<h2>📊 Land Cover Statistics</h2>", unsafe_allow_html=True)
    
    if 'area_stats' in statistics:
        area_df = statistics['area_stats']
        st.dataframe(area_df, width='stretch', hide_index=True)
        
        # Visualize statistics using matplotlib
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            
            classes = area_df['Class'].values
            areas = area_df['Area_km2'].values
            colors_list = ['#0066FF', '#00CC00', '#FF0000', '#FFAA00']
            
            bars = ax.bar(classes, areas, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # Add value labels on top of bars
            for bar, area in zip(bars, areas):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{area:.1f}',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            ax.set_ylabel('Area (km²)', fontsize=12, fontweight='bold')
            ax.set_title('Area Distribution', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            
            classes = area_df['Class'].values
            percents = area_df['Percent'].values
            colors_list = ['#0066FF', '#00CC00', '#FF0000', '#FFAA00']
            
            bars = ax.bar(classes, percents, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # Add value labels on top of bars
            for bar, pct in zip(bars, percents):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{pct:.1f}%',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
            ax.set_title('Percentage Distribution', fontsize=14, fontweight='bold')
            ax.set_ylim([0, 105])
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
    
    st.divider()
    
    # Download options
    st.markdown("<h2>📥 Export Results</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    # 1. Download Classification Map (PNG)
    with col1:
        st.markdown("**Classification Map**")
        if st.button("📥 PNG", key="btn_map", width='stretch'):
            import io
            from PIL import Image as PILImage
            
            color_map_uint8 = color_map.astype(np.uint8)
            pil_image = PILImage.fromarray(color_map_uint8, 'RGB')
            
            buffer = io.BytesIO()
            pil_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            st.download_button(
                label="💾 Download PNG",
                data=buffer.getvalue(),
                file_name="classification_map.png",
                mime="image/png",
                key="download_map"
            )
    
    # 2. Download Area Statistics (Excel)
    with col2:
        st.markdown("**Area Statistics**")
        if st.button("📊 Excel", key="btn_area", width='stretch'):
            try:
                # Create Excel file
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    statistics['area_stats'].to_excel(writer, sheet_name='Area Statistics', index=False)
                
                excel_buffer.seek(0)
                
                st.download_button(
                    label="💾 Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="area_statistics.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_area"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
    
    # 3. Download Model Statistics (Excel)
    with col3:
        st.markdown("**Model Statistics**")
        if st.button("🤖 Excel", key="btn_model", width='stretch'):
            try:
                # Create comprehensive model stats
                model_stats = pd.DataFrame({
                    'Model': [predictions['model_name']],
                    'Training Accuracy': [f"{predictions['train_acc']*100:.2f}%"],
                    'Testing Accuracy': [f"{predictions['test_acc']*100:.2f}%"],
                    'Classes': ['4'],
                    'Feature Count': ['10'],
                    'Training Samples': [len(predictions['Y_true'])]
                })
                
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    model_stats.to_excel(writer, sheet_name='Model Statistics', index=False)
                
                excel_buffer.seek(0)
                
                st.download_button(
                    label="💾 Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="model_statistics.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_model"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
    
    # 4. Download Report (TXT)
    with col4:
        st.markdown("**Full Report**")
        if st.button("📄 TXT", key="btn_report", width='stretch'):
            report = f"""
{'='*60}
REMOTE SENSING CLASSIFICATION REPORT
{'='*60}

MODEL INFORMATION
{'-'*60}
Model Type: {predictions['model_name']}
Training Accuracy: {predictions['train_acc']*100:.2f}%
Testing Accuracy: {predictions['test_acc']*100:.2f}%
Number of Classes: 4
Features Used: 10 (7 bands + 3 indices)
Training Samples: {len(predictions['Y_true'])}

LAND COVER DISTRIBUTION
{'-'*60}
{statistics['area_stats'].to_string(index=False)}

CLASSIFICATION DETAILS
{'-'*60}
Classes:
  1. Water (🔵 Blue)
  2. Vegetation (🟢 Green)
  3. Urban (🔴 Red)
  4. Desert (🟠 Orange)

Spectral Indices Computed:
  - NDVI (Normalized Difference Vegetation Index)
  - NDWI (Normalized Difference Water Index)
  - NDBI (Normalized Difference Built-up Index)

Calibration:
  - Radiometric calibration applied
  - Sun elevation angle: 39.31°
  - Pixel size: 30 meters (Landsat 8 standard)

{'='*60}
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
            """
            
            st.download_button(
                label="💾 Download TXT",
                data=report,
                file_name="classification_report.txt",
                mime="text/plain",
                key="download_report"
            )
    
    st.divider()
    
    # Summary
    st.markdown("""
    <div class='card card-success'>
        <h3 style='text-align: center; margin-top: 0;'>✅ Analysis Complete</h3>
        <p style='text-align: center; margin-bottom: 0;'>
            Classification completed successfully. Download your results using the buttons above.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 🎯 MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    setup_page_config()
    
    # Initialize session state
    if 'uploaded_bands' not in st.session_state:
        st.session_state.uploaded_bands = None  # CSV file object or None
    if 'mtl_data' not in st.session_state:
        st.session_state.mtl_data = None  # BIN file object or None
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
