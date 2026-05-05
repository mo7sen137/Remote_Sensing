"""
Unit Tests for Preprocessor Module
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessor import RadiometricCalibration


class TestRadiometricCalibration(unittest.TestCase):
    """Test radiometric calibration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mtl_metadata = {
            'ML_B2': 0.0001,
            'AL_B2': 0.0,
            'ML_B3': 0.0001,
            'AL_B3': 0.0,
            'ML_B4': 0.0001,
            'AL_B4': 0.0,
            'ML_B5': 0.0001,
            'AL_B5': 0.0,
            'ML_B6': 0.00005,
            'AL_B6': 0.0,
            'ML_B7': 0.00005,
            'AL_B7': 0.0,
            'SUN_ELEVATION_ANGLE': 45.0
        }
        
        self.calibrator = RadiometricCalibration(self.mtl_metadata)
    
    def test_dn_to_toa_reflectance_shape(self):
        """Test output shape matches input shape."""
        dn_array = np.random.randint(0, 10000, (100, 100), dtype=np.uint16)
        result = self.calibrator.dn_to_toa_reflectance(dn_array, 4)
        
        self.assertEqual(result.shape, dn_array.shape)
    
    def test_toa_reflectance_range(self):
        """Test output values are in valid range [0, 1]."""
        dn_array = np.random.randint(0, 10000, (100, 100), dtype=np.uint16)
        result = self.calibrator.dn_to_toa_reflectance(dn_array, 4)
        
        self.assertGreaterEqual(np.min(result), 0.0)
        self.assertLessEqual(np.max(result), 1.0)
    
    def test_calibrate_multiple_bands(self):
        """Test calibrating multiple bands."""
        bands = {
            2: np.random.randint(0, 10000, (50, 50), dtype=np.uint16),
            3: np.random.randint(0, 10000, (50, 50), dtype=np.uint16),
            4: np.random.randint(0, 10000, (50, 50), dtype=np.uint16),
        }
        
        result = self.calibrator.calibrate_bands(bands)
        
        self.assertEqual(len(result), 3)
        for band_num in [2, 3, 4]:
            self.assertIn(band_num, result)
            self.assertEqual(result[band_num].shape, (50, 50))


if __name__ == '__main__':
    unittest.main()
