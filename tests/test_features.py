"""
Unit Tests for Feature Extraction Module
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.feature_extractor import SpectralIndicesExtractor


class TestSpectralIndices(unittest.TestCase):
    """Test spectral indices calculation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.height, self.width = 50, 50
        self.red = np.random.uniform(0, 1, (self.height, self.width))
        self.nir = np.random.uniform(0, 1, (self.height, self.width))
        self.swir1 = np.random.uniform(0, 1, (self.height, self.width))
    
    def test_ndvi_range(self):
        """Test NDVI is in valid range [-1, 1]."""
        ndvi = SpectralIndicesExtractor.calculate_ndvi(self.red, self.nir)
        
        self.assertGreaterEqual(np.min(ndvi), -1.0)
        self.assertLessEqual(np.max(ndvi), 1.0)
    
    def test_ndwi_range(self):
        """Test NDWI is in valid range [-1, 1]."""
        ndwi = SpectralIndicesExtractor.calculate_ndwi(self.nir, self.swir1)
        
        self.assertGreaterEqual(np.min(ndwi), -1.0)
        self.assertLessEqual(np.max(ndwi), 1.0)
    
    def test_ndbi_range(self):
        """Test NDBI is in valid range [-1, 1]."""
        ndbi = SpectralIndicesExtractor.calculate_ndbi(self.swir1, self.nir)
        
        self.assertGreaterEqual(np.min(ndbi), -1.0)
        self.assertLessEqual(np.max(ndbi), 1.0)
    
    def test_feature_stack_shape(self):
        """Test feature stack has correct shape."""
        bands = {
            2: self.red, 3: self.red, 4: self.red,
            5: self.nir, 6: self.swir1, 7: self.red
        }
        indices = {
            'NDVI': SpectralIndicesExtractor.calculate_ndvi(self.red, self.nir),
            'NDWI': SpectralIndicesExtractor.calculate_ndwi(self.nir, self.swir1),
            'NDBI': SpectralIndicesExtractor.calculate_ndbi(self.swir1, self.nir)
        }
        
        stack = SpectralIndicesExtractor.create_feature_stack(bands, indices)
        
        self.assertEqual(stack.shape, (self.height, self.width, 10))


if __name__ == '__main__':
    unittest.main()
