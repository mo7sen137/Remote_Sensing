"""
Callback Functions and Event Handlers
Handles the core processing logic triggered by UI events
"""

import streamlit as st
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessor import RadiometricCalibration
from src.feature_extractor import SpectralIndicesExtractor
from src.classifier import LandClassifier
from src.postprocessor import MapGenerator
from src.utils import LandsatFileHandler, Validator


def handle_file_upload(uploaded_files: dict, mtl_file) -> dict:
    """
    Process uploaded files and load bands.
    
    Args:
        uploaded_files: Dictionary of uploaded band files
        mtl_file: Uploaded MTL metadata file
        
    Returns:
        Dictionary with processing results
    """
    
    results = {
        'success': False,
        'bands': None,
        'mtl_metadata': None,
        'message': ''
    }
    
    try:
        # Load MTL metadata
        if mtl_file:
            mtl_content = mtl_file.read().decode('utf-8')
            mtl_metadata = RadiometricCalibration.parse_mtl_file(mtl_file)
            results['mtl_metadata'] = mtl_metadata
        
        # Load bands
        bands = {}
        for band_num, file in uploaded_files.items():
            # Save temporarily and load
            with open(f'/tmp/band_{band_num}.tif', 'wb') as f:
                f.write(file.getbuffer())
            
            band_data = LandsatFileHandler.load_band(f'/tmp/band_{band_num}.tif')
            bands[band_num] = band_data
        
        # Validate all bands have same shape
        Validator.validate_band_shape(bands)
        
        results['bands'] = bands
        results['success'] = True
        results['message'] = f'✓ Loaded {len(bands)} bands'
        
    except Exception as e:
        results['message'] = f'✗ Error: {str(e)}'
    
    return results


def run_classification(bands: dict, mtl_metadata: dict, 
                       model_name: str, model_path: str) -> dict:
    """
    Execute complete classification pipeline.
    
    Args:
        bands: Dictionary of band arrays
        mtl_metadata: MTL metadata for calibration
        model_name: Name of model to use
        model_path: Path to trained model file
        
    Returns:
        Dictionary with predictions and statistics
    """
    
    results = {
        'success': False,
        'predictions': None,
        'rgb_map': None,
        'statistics': None,
        'message': ''
    }
    
    try:
        # Step 1: Radiometric Calibration
        st.write("Step 1/4: Radiometric Calibration...")
        calibrator = RadiometricCalibration(mtl_metadata)
        calibrated_bands = calibrator.calibrate_bands(bands)
        
        # Step 2: Feature Extraction
        st.write("Step 2/4: Extracting Spectral Indices...")
        extractor = SpectralIndicesExtractor()
        indices = extractor.extract_all_indices(calibrated_bands)
        feature_stack = extractor.create_feature_stack(calibrated_bands, indices)
        
        # Step 3: Load Model and Predict
        st.write("Step 3/4: Running Classification...")
        classifier = LandClassifier(model_path)
        height, width = bands[2].shape
        predictions = classifier.predict(feature_stack)
        
        # Step 4: Generate Map and Statistics
        st.write("Step 4/4: Generating Map and Statistics...")
        map_generator = MapGenerator()
        rgb_map = map_generator.predictions_to_rgb(predictions, height, width)
        statistics = map_generator.calculate_areas(predictions, height, width)
        
        results['predictions'] = predictions
        results['rgb_map'] = rgb_map
        results['statistics'] = statistics
        results['success'] = True
        results['message'] = '✓ Classification complete!'
        
    except Exception as e:
        results['message'] = f'✗ Error during classification: {str(e)}'
    
    return results


def validate_input_data(bands: dict) -> tuple:
    """
    Validate input data before processing.
    
    Args:
        bands: Dictionary of band arrays
        
    Returns:
        Tuple of (is_valid, message)
    """
    
    # Check if all required bands present
    required_bands = [2, 3, 4, 5, 6, 7]
    missing_bands = [b for b in required_bands if b not in bands]
    
    if missing_bands:
        return False, f"Missing bands: {missing_bands}"
    
    # Check for valid data range (0-65535 for DN, or 0-1 for reflectance)
    for band_num, data in bands.items():
        if np.any(np.isnan(data)):
            return False, f"Band {band_num} contains NaN values"
    
    return True, "✓ Input validation passed"
