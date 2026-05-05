"""
Spectral Indices Extractor Module
Calculates vegetation, water, and urbanization indices
"""

import numpy as np
from typing import Dict, Tuple


class SpectralIndicesExtractor:
    """
    Calculates spectral indices (NDVI, NDWI, NDBI) from calibrated Landsat 8 bands.
    """
    
    @staticmethod
    def calculate_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Vegetation Index (NDVI).
        
        Formula: NDVI = (NIR - Red) / (NIR + Red)
        Range: [-1, 1]
        Vegetation appears green in visualization
        
        Args:
            red: Red band reflectance (Band 4)
            nir: Near-Infrared band reflectance (Band 5)
            
        Returns:
            2D array of NDVI values
        """
        denominator = nir + red
        # Avoid division by zero
        denominator = np.where(denominator == 0, 1e-10, denominator)
        
        ndvi = (nir - red) / denominator
        return np.clip(ndvi, -1, 1)
    
    @staticmethod
    def calculate_ndwi(nir: np.ndarray, swir1: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Water Index (NDWI).
        
        Formula: NDWI = (NIR - SWIR1) / (NIR + SWIR1)
        Range: [-1, 1]
        Water appears blue in visualization
        
        Args:
            nir: Near-Infrared band reflectance (Band 5)
            swir1: Shortwave Infrared 1 reflectance (Band 6)
            
        Returns:
            2D array of NDWI values
        """
        denominator = nir + swir1
        denominator = np.where(denominator == 0, 1e-10, denominator)
        
        ndwi = (nir - swir1) / denominator
        return np.clip(ndwi, -1, 1)
    
    @staticmethod
    def calculate_ndbi(swir1: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Built-up Index (NDBI).
        
        Formula: NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
        Range: [-1, 1]
        Urban areas appear red in visualization
        
        Args:
            swir1: Shortwave Infrared 1 reflectance (Band 6)
            nir: Near-Infrared band reflectance (Band 5)
            
        Returns:
            2D array of NDBI values
        """
        denominator = swir1 + nir
        denominator = np.where(denominator == 0, 1e-10, denominator)
        
        ndbi = (swir1 - nir) / denominator
        return np.clip(ndbi, -1, 1)
    
    @staticmethod
    def extract_all_indices(bands: Dict[int, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Extract all spectral indices from calibrated bands.
        
        Args:
            bands: Dictionary with band numbers and their reflectance arrays
                  Must contain: 4 (Red), 5 (NIR), 6 (SWIR1)
                  
        Returns:
            Dictionary with keys: 'NDVI', 'NDWI', 'NDBI'
        """
        red = bands.get(4)
        nir = bands.get(5)
        swir1 = bands.get(6)
        
        if red is None or nir is None or swir1 is None:
            raise ValueError("Required bands (4, 5, 6) not found in input")
        
        indices = {
            'NDVI': SpectralIndicesExtractor.calculate_ndvi(red, nir),
            'NDWI': SpectralIndicesExtractor.calculate_ndwi(nir, swir1),
            'NDBI': SpectralIndicesExtractor.calculate_ndbi(swir1, nir),
        }
        
        return indices
    
    @staticmethod
    def create_feature_stack(bands: Dict[int, np.ndarray], 
                            indices: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Stack all bands and indices into a 3D feature array.
        
        Args:
            bands: Calibrated bands (2-7)
            indices: Calculated spectral indices (NDVI, NDWI, NDBI)
            
        Returns:
            3D array of shape (height, width, 10) with all features
        """
        # Get dimensions from first band
        height, width = next(iter(bands.values())).shape
        
        # Initialize feature stack (7 bands + 3 indices = 10 features)
        feature_stack = np.zeros((height, width, 10), dtype=np.float32)
        
        # Add the 6 reflectance bands (2-7)
        for idx, band_num in enumerate([2, 3, 4, 5, 6, 7]):
            feature_stack[:, :, idx] = bands[band_num]
        
        # Add spectral indices
        feature_stack[:, :, 6] = indices['NDVI']
        feature_stack[:, :, 7] = indices['NDWI']
        feature_stack[:, :, 8] = indices['NDBI']
        
        # Feature 9 is available for future use (e.g., MNDWI, EVI, etc.)
        
        return feature_stack
