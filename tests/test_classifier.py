"""
Unit Tests for Classifier Module
"""

import unittest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.classifier import LandClassifier


class TestLandClassifier(unittest.TestCase):
    """Test classification functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.height, self.width = 50, 50
        self.n_features = 10
        self.feature_stack = np.random.uniform(0, 1, 
                                               (self.height, self.width, self.n_features))
    
    def test_reshape_to_samples(self):
        """Test reshaping feature stack to samples."""
        classifier = LandClassifier()
        samples = classifier.reshape_to_samples(self.feature_stack)
        
        expected_n_samples = self.height * self.width
        self.assertEqual(samples.shape, (expected_n_samples, self.n_features))
    
    def test_reshape_preserves_data(self):
        """Test reshape preserves data values."""
        classifier = LandClassifier()
        samples = classifier.reshape_to_samples(self.feature_stack)
        
        # Check that unique values are preserved
        original_unique = np.unique(self.feature_stack)
        reshaped_unique = np.unique(samples)
        
        self.assertTrue(np.allclose(np.sort(original_unique), 
                                   np.sort(reshaped_unique)))


if __name__ == '__main__':
    unittest.main()
