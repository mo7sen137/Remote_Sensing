"""
Utility Functions Module
Helper functions for data loading, validation, and processing
"""

import os
import numpy as np
from typing import Dict, Tuple, List
import tifffile


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
