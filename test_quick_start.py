"""
Quick Start Script for Testing the Pipeline
Run this to verify all components are working
"""

import sys
from pathlib import Path
import numpy as np

# Add project to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    try:
        from src.preprocessor import RadiometricCalibration
        from src.feature_extractor import SpectralIndicesExtractor
        from src.classifier import LandClassifier
        from src.postprocessor import MapGenerator
        from src.utils import LandsatFileHandler, Validator
        import config
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_calibration():
    """Test radiometric calibration."""
    print("\n🔬 Testing Radiometric Calibration...")
    try:
        from src.preprocessor import RadiometricCalibration
        
        mtl_data = {
            'ML_B4': 0.0001, 'AL_B4': 0.0,
            'ML_B5': 0.0001, 'AL_B5': 0.0,
            'SUN_ELEVATION_ANGLE': 45.0
        }
        
        calibrator = RadiometricCalibration(mtl_data)
        
        # Create test DN array
        dn = np.random.randint(0, 10000, (100, 100), dtype=np.uint16)
        reflectance = calibrator.dn_to_toa_reflectance(dn, 4)
        
        assert reflectance.shape == (100, 100)
        assert np.all(reflectance >= 0) and np.all(reflectance <= 1)
        print("  ✅ Calibration test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_indices():
    """Test spectral indices calculation."""
    print("\n📈 Testing Spectral Indices...")
    try:
        from src.feature_extractor import SpectralIndicesExtractor
        
        red = np.random.uniform(0, 1, (100, 100))
        nir = np.random.uniform(0, 1, (100, 100))
        swir1 = np.random.uniform(0, 1, (100, 100))
        
        ndvi = SpectralIndicesExtractor.calculate_ndvi(red, nir)
        ndwi = SpectralIndicesExtractor.calculate_ndwi(nir, swir1)
        ndbi = SpectralIndicesExtractor.calculate_ndbi(swir1, nir)
        
        assert ndvi.shape == (100, 100)
        assert np.all(ndvi >= -1) and np.all(ndvi <= 1)
        assert np.all(ndwi >= -1) and np.all(ndwi <= 1)
        assert np.all(ndbi >= -1) and np.all(ndbi <= 1)
        
        print("  ✅ Spectral indices test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_postprocessing():
    """Test map generation."""
    print("\n🗺️ Testing Map Generation...")
    try:
        from src.postprocessor import MapGenerator
        
        predictions = np.random.randint(0, 4, 10000)
        map_gen = MapGenerator()
        
        rgb = map_gen.predictions_to_rgb(predictions, 100, 100)
        
        assert rgb.shape == (100, 100, 3)
        assert rgb.dtype == np.uint8
        
        print("  ✅ Map generation test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🛰️  REMOTE SENSING - QUICK START TEST SUITE")
    print("=" * 60)
    
    results = {
        'Imports': test_imports(),
        'Calibration': test_calibration(),
        'Indices': test_indices(),
        'Postprocessing': test_postprocessing(),
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "=" * 60)
    print(f"Score: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All systems operational! Ready to deploy.")
        print("\nNext steps:")
        print("  1. Place trained models in /models/ directory")
        print("  2. Run: streamlit run app/main.py")
        print("  3. Upload Landsat data through web interface")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
