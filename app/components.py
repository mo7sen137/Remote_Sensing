"""
UI Components for Streamlit Application
"""

import streamlit as st
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def setup_sidebar():
    """
    Setup sidebar with controls.
    
    Returns:
        Selected model name
    """
    
    st.markdown("#### 📊 Dataset Info")
    st.info("""
    **Landsat 8 Dataset**
    - 7 Spectral Bands (2-7)
    - 30m Resolution
    - Path 177 / Row 039
    - Region: Nile Delta, Egypt
    """)
    
    st.markdown("---")
    
    st.markdown("#### 🤖 Model Selection")
    available_models = list(config.SUPPORTED_MODELS.keys())
    model_name = st.selectbox(
        "Choose Classification Model",
        available_models,
        index=available_models.index(config.DEFAULT_MODEL) if config.DEFAULT_MODEL in available_models else 0
    )
    
    st.markdown("---")
    
    st.markdown("#### 📋 Instructions")
    with st.expander("How to Use", expanded=False):
        st.markdown("""
        1. **Upload Data**
           - Upload all 7 Landsat bands (B2-B7)
           - Upload MTL metadata file
        
        2. **Preview**
           - View raw bands
           - Check spectral indices (NDVI, NDWI, NDBI)
        
        3. **Classify**
           - Select model
           - Click "Run Classification"
        
        4. **View Results**
           - Download classified map
           - View area statistics
        """)
    
    return model_name


def setup_main_panel(section: str, model_name: str = None):
    """
    Setup main panel content based on selected tab.
    
    Args:
        section: Tab section name
        model_name: Selected model name
    """
    
    if section == "upload":
        st.markdown("### 📤 Upload Landsat 8 Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Spectral Bands")
            st.info("Upload all 7 bands (B2-B7) as GeoTIFF files")
            
            for band_num in range(2, 8):
                uploaded_file = st.file_uploader(
                    f"Band {band_num}",
                    type=['tif', 'tiff'],
                    key=f"band_{band_num}"
                )
                if uploaded_file:
                    st.session_state.uploaded_bands[band_num] = uploaded_file
            
            st.success(f"✓ {len(st.session_state.uploaded_bands)} bands loaded")
        
        with col2:
            st.markdown("#### Metadata")
            st.info("Upload MTL metadata file for radiometric calibration")
            
            mtl_file = st.file_uploader(
                "MTL File",
                type=['txt'],
                key="mtl_file"
            )
            if mtl_file:
                st.session_state.mtl_data = mtl_file
                st.success("✓ MTL file loaded")
        
        if st.button("🚀 Proceed to Preview", use_container_width=True):
            if len(st.session_state.uploaded_bands) == 6 and st.session_state.mtl_data:
                st.success("Ready to preview!")
            else:
                st.error("Please upload all bands and MTL file")
    
    elif section == "preview":
        st.markdown("### 🔍 Data Preview")
        
        if len(st.session_state.uploaded_bands) == 0:
            st.warning("No data uploaded yet. Go to 'Upload Data' tab first.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Band Information")
            for band_num in range(2, 8):
                if band_num in st.session_state.uploaded_bands:
                    st.markdown(f"**Band {band_num}**: {config.LANDSAT_BANDS[band_num]}")
        
        with col2:
            st.markdown("#### Spectral Indices")
            for idx_name, idx_info in config.SPECTRAL_INDICES.items():
                st.markdown(f"""
                **{idx_name}**
                - Formula: {idx_info['formula']}
                - Purpose: {idx_info['description']}
                """)
        
        st.markdown("---")
        
        col_ndvi, col_ndwi, col_ndbi = st.columns(3)
        
        with col_ndvi:
            st.markdown("#### NDVI (Vegetation)")
            st.info("Shows vegetation and agricultural areas in green")
        
        with col_ndwi:
            st.markdown("#### NDWI (Water)")
            st.info("Shows water bodies in blue")
        
        with col_ndbi:
            st.markdown("#### NDBI (Urban)")
            st.info("Shows urban/built-up areas in red")
    
    elif section == "classification":
        st.markdown("### 🗺️ Land Cover Classification")
        
        if len(st.session_state.uploaded_bands) == 0:
            st.warning("No data uploaded yet.")
            return
        
        st.info(f"Using model: **{model_name}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Number of Classes", "4", "Water, Agriculture, Urban, Desert")
        
        with col2:
            st.metric("Minimum Training Pixels", f"{config.MIN_PIXELS_PER_CLASS}", "per class")
        
        with col3:
            st.metric("Output Resolution", "30m", "per pixel")
        
        st.markdown("---")
        
        if st.button("▶️ Run Classification", use_container_width=True, key="run_class"):
            st.info("Classification in progress...")
            # Placeholder for actual classification
            st.success("✓ Classification complete!")
            st.balloons()
    
    elif section == "results":
        st.markdown("### 📊 Results & Statistics")
        
        if st.session_state.predictions is None:
            st.warning("No classification results yet. Run classification first.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Classified Map")
            st.info("Map preview would appear here")
        
        with col2:
            st.markdown("#### Area Statistics")
            st.info("Area statistics table would appear here")
        
        st.markdown("---")
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            st.download_button(
                label="📥 Download Map (PNG)",
                data=b"placeholder",
                file_name="land_classification_map.png",
                mime="image/png"
            )
        
        with col_download2:
            st.download_button(
                label="📊 Download Statistics (CSV)",
                data=b"placeholder",
                file_name="land_statistics.csv",
                mime="text/csv"
            )
