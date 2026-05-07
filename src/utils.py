"""
Utility Functions Module
Helper functions for data loading, validation, and processing
"""

import os
import numpy as np
from typing import Dict, Tuple, List
import tifffile
from io import BytesIO


# ============================================================================
# FILE VALIDATION - Secure File Upload Validation
# ============================================================================

class FileValidator:
    """
    Comprehensive file validation for uploaded files.
    Prevents malicious uploads and corrupted data.
    """
    
    # Configuration
    MAX_FILE_SIZE_MB = 100  # Maximum 100MB per file
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS = {'.tif', '.tiff', '.txt'}
    MAX_DIMENSION = 5000  # Maximum 5000x5000 pixels
    MIN_DIMENSION = 100   # Minimum 100x100 pixels
    
    @staticmethod
    def validate_geotiff_file(file_obj, filename: str) -> Tuple[bool, str]:
        """
        Validate GeoTIFF file for security and integrity.
        
        Args:
            file_obj: File object from streamlit uploader
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # 1. Check file extension
            if not any(filename.lower().endswith(ext) for ext in ['.tif', '.tiff']):
                return False, f"❌ Invalid file type. Expected .tif or .tiff, got {os.path.splitext(filename)[1]}"
            
            # 2. Check file size
            file_size = len(file_obj.getbuffer()) if hasattr(file_obj, 'getbuffer') else len(file_obj)
            if file_size > FileValidator.MAX_FILE_SIZE_BYTES:
                size_mb = file_size / (1024 * 1024)
                return False, f"❌ File too large: {size_mb:.1f}MB (max: {FileValidator.MAX_FILE_SIZE_MB}MB)"
            
            if file_size < 1024:  # Less than 1KB
                return False, "❌ File too small (possibly empty or corrupted)"
            
            # 3. Validate file content
            try:
                file_bytes = file_obj.getbuffer() if hasattr(file_obj, 'getbuffer') else file_obj.read()
                with tifffile.TiffFile(BytesIO(file_bytes)) as tif:
                    # Check if it's a valid TIFF
                    if not tif.is_tiled and len(tif.pages) == 0:
                        return False, "❌ Invalid TIFF file (no pages)"
                    
                    # Get image dimensions
                    page = tif.pages[0]
                    height, width = page.shape[:2]
                    
                    # Validate dimensions
                    if width < FileValidator.MIN_DIMENSION or height < FileValidator.MIN_DIMENSION:
                        return False, f"❌ Image too small: {width}x{height} (min: {FileValidator.MIN_DIMENSION}x{FileValidator.MIN_DIMENSION})"
                    
                    if width > FileValidator.MAX_DIMENSION or height > FileValidator.MAX_DIMENSION:
                        return False, f"❌ Image too large: {width}x{height} (max: {FileValidator.MAX_DIMENSION}x{FileValidator.MAX_DIMENSION})"
                    
                    # Check for reasonable data type (uint8, uint16, float32, float64)
                    dtype_str = str(page.dtype)
                    valid_dtypes = ['uint8', 'uint16', 'uint32', 'float32', 'float64', 'int16', 'int32']
                    if not any(dt in dtype_str for dt in valid_dtypes):
                        return False, f"❌ Unsupported data type: {page.dtype}"
                    
                    return True, f"✅ Valid GeoTIFF: {width}x{height} pixels, {page.dtype}"
                    
            except Exception as e:
                return False, f"❌ File is corrupted or not a valid TIFF: {str(e)}"
        
        except Exception as e:
            return False, f"❌ Validation error: {str(e)}"
    
    @staticmethod
    def validate_mtl_file(file_obj, filename: str) -> Tuple[bool, str]:
        """
        Validate MTL metadata file.
        
        Args:
            file_obj: File object from streamlit uploader
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check extension
            if not filename.lower().endswith('.txt'):
                return False, "❌ MTL file must be .txt format"
            
            # Check file size (MTL files are usually < 1MB)
            file_size = len(file_obj.getbuffer()) if hasattr(file_obj, 'getbuffer') else len(file_obj)
            if file_size > 5 * 1024 * 1024:  # 5MB max
                return False, "❌ MTL file too large (max 5MB)"
            
            if file_size < 100:  # Less than 100 bytes
                return False, "❌ MTL file too small (possibly corrupted)"
            
            # Read and validate content
            content = file_obj.read().decode('utf-8', errors='ignore')
            
            # Check for required MTL keys
            required_keys = ['LANDSAT_SCENE_ID', 'RADIANCE', 'REFLECTANCE']
            has_required = any(key in content for key in required_keys)
            
            if not has_required:
                return False, "❌ MTL file missing required Landsat metadata"
            
            return True, "✅ Valid MTL metadata file"
        
        except Exception as e:
            return False, f"❌ MTL validation error: {str(e)}"
    
    @staticmethod
    def validate_band_consistency(bands: Dict[int, np.ndarray]) -> Tuple[bool, str]:
        """
        Validate that all bands have consistent dimensions.
        
        Args:
            bands: Dictionary of loaded band arrays
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            if not bands:
                return False, "❌ No bands provided"
            
            # Get first band dimensions
            first_band = next(iter(bands.values()))
            expected_shape = first_band.shape
            
            # Check all bands match
            for band_num, band_data in bands.items():
                if band_data.shape != expected_shape:
                    return False, f"❌ Band {band_num} has inconsistent shape: {band_data.shape} vs expected {expected_shape}"
                
                # Check for NaN values
                if np.isnan(band_data).any():
                    nan_count = np.isnan(band_data).sum()
                    if nan_count > len(band_data.flat) * 0.1:  # More than 10% NaN
                        return False, f"❌ Band {band_num} has too many NaN values ({nan_count})"
            
            return True, f"✅ All {len(bands)} bands are consistent: {expected_shape}"
        
        except Exception as e:
            return False, f"❌ Consistency check error: {str(e)}"



class LandsatFileHandler:
    """
    Handle Landsat 8 file I/O operations.
    """
    
    @staticmethod
    def load_band(filepath: str) -> np.ndarray:
        """
        Load a single band from GeoTIFF file.
        
        Args:
            filepath: Path to GeoTIFF file
            
        Returns:
            2D numpy array of band data
        """
        try:
            band_data = tifffile.imread(filepath)
            return band_data
        except Exception as e:
            raise IOError(f"Error reading band file {filepath}: {str(e)}")
    
    @staticmethod
    def load_multiple_bands(band_paths: Dict[int, str]) -> Dict[int, np.ndarray]:
        """
        Load multiple bands from files.
        
        Args:
            band_paths: Dictionary mapping band numbers to file paths
            
        Returns:
            Dictionary with band numbers and loaded arrays
        """
        bands = {}
        
        for band_num, filepath in band_paths.items():
            try:
                bands[band_num] = LandsatFileHandler.load_band(filepath)
                print(f"✓ Loaded Band {band_num}")
            except Exception as e:
                print(f"✗ Error loading Band {band_num}: {str(e)}")
        
        return bands
    
    @staticmethod
    def validate_band_shape(bands: Dict[int, np.ndarray]) -> Tuple[int, int]:
        """
        Validate that all bands have the same shape.
        
        Args:
            bands: Dictionary of band arrays
            
        Returns:
            Tuple of (height, width)
            
        Raises:
            ValueError: If bands have different shapes
        """
        if not bands:
            raise ValueError("No bands provided")
        
        first_shape = next(iter(bands.values())).shape
        
        for band_num, array in bands.items():
            if array.shape != first_shape:
                raise ValueError(
                    f"Band {band_num} has shape {array.shape}, "
                    f"expected {first_shape}"
                )
        
        return first_shape
    
    @staticmethod
    def crop_bands(bands: Dict[int, np.ndarray], 
                   row_start: int, row_end: int,
                   col_start: int, col_end: int) -> Dict[int, np.ndarray]:
        """
        Crop all bands to specified region.
        
        Args:
            bands: Dictionary of band arrays
            row_start, row_end: Row range
            col_start, col_end: Column range
            
        Returns:
            Dictionary of cropped bands
        """
        cropped = {}
        
        for band_num, array in bands.items():
            cropped[band_num] = array[row_start:row_end, col_start:col_end]
        
        return cropped


class TrainingDataHandler:
    """
    Handle training/validation data from ENVI ROI exports.
    """
    
    @staticmethod
    def load_training_csv(csv_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load training data from CSV (exported from ENVI).
        
        Expected format:
        - Columns for each of 10 features (7 bands + 3 indices)
        - Last column is class label
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Tuple of (features, labels) numpy arrays
        """
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            # Assume last column is label
            features = df.iloc[:, :-1].values.astype(np.float32)
            labels = df.iloc[:, -1].values.astype(np.int32)
            
            return features, labels
        except Exception as e:
            raise IOError(f"Error loading training CSV: {str(e)}")
    
    @staticmethod
    def split_train_test(features: np.ndarray, labels: np.ndarray,
                        train_ratio: float = 0.7) -> Tuple:
        """
        Split data into train/test sets.
        
        Args:
            features: Feature array
            labels: Label array
            train_ratio: Fraction for training (default 0.7)
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        n_samples = len(features)
        n_train = int(n_samples * train_ratio)
        
        # Shuffle indices
        indices = np.random.permutation(n_samples)
        
        train_idx = indices[:n_train]
        test_idx = indices[n_train:]
        
        X_train = features[train_idx]
        X_test = features[test_idx]
        y_train = labels[train_idx]
        y_test = labels[test_idx]
        
        return X_train, X_test, y_train, y_test


class Validator:
    """
    Validation utilities for input data.
    """
    
    @staticmethod
    def check_file_exists(filepath: str) -> bool:
        """Check if file exists."""
        return os.path.isfile(filepath)
    
    @staticmethod
    def check_directory_exists(dirpath: str) -> bool:
        """Check if directory exists."""
        return os.path.isdir(dirpath)
    
    @staticmethod
    def validate_bands_in_range(bands: Dict[int, np.ndarray],
                               expected_range: Tuple[float, float] = (0, 1)) -> bool:
        """
        Validate that band values are in expected range.
        
        Args:
            bands: Dictionary of band arrays
            expected_range: Tuple of (min, max) expected values
            
        Returns:
            True if all values in range, False otherwise
        """
        min_val, max_val = expected_range
        
        for band_num, array in bands.items():
            if np.any(array < min_val) or np.any(array > max_val):
                print(f"Warning: Band {band_num} has values outside "
                      f"expected range [{min_val}, {max_val}]")
                print(f"  Actual range: [{np.min(array):.4f}, {np.max(array):.4f}]")
                return False
        
        return True


class ProgressTracker:
    """
    Simple progress tracking for long operations.
    """
    
    def __init__(self, total_items: int, description: str = "Processing"):
        self.total = total_items
        self.current = 0
        self.description = description
    
    def update(self, n: int = 1) -> None:
        """Update progress."""
        self.current += n
        percentage = (self.current / self.total) * 100
        print(f"\r{self.description}: {percentage:.1f}%", end="")
    
    def finish(self) -> None:
        """Mark completion."""
        print(f"\r{self.description}: 100.0% ✓")
