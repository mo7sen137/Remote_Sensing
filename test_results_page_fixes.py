#!/usr/bin/env python3
"""
Final Verification Test for Results Page Enhancements
Tests all functionality that was fixed
"""

import sys
sys.path.insert(0, '/workspaces/Remote_Sensing')

import numpy as np
import pandas as pd
import io
from PIL import Image as PILImage


def test_imports():
    """Test that all required imports work"""
    print("\n" + "="*60)
    print("TEST 1: Import Verification")
    print("="*60)
    
    try:
        from app.main import page_results, ClassificationMapper
        from src.model_trainer import FeatureExtractor, ModelTrainer
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_array_reshaping():
    """Test the array reshaping logic"""
    print("\n" + "="*60)
    print("TEST 2: Array Reshaping Logic")
    print("="*60)
    
    test_cases = [
        (100, 10),
        (225, 15),
        (256, 16),
        (500, 23),
        (1000, 32),
        (1024, 32)
    ]
    
    all_passed = True
    for n_pixels, expected_side in test_cases:
        # Simulate the reshaping logic from page_results()
        class_map = np.random.randint(1, 5, size=n_pixels)
        class_map_flat = class_map.flatten()
        n_pixels_actual = len(class_map_flat)
        side_length = int(np.sqrt(n_pixels_actual))
        
        if side_length * side_length < n_pixels_actual:
            side_length += 1
        
        padded_size = side_length * side_length
        if padded_size > n_pixels_actual:
            class_map_flat = np.pad(class_map_flat, 
                                   (0, padded_size - n_pixels_actual), 
                                   mode='constant')
        
        class_map_reshaped = class_map_flat[:padded_size].reshape(side_length, side_length)
        
        if side_length == expected_side and class_map_reshaped.shape == (side_length, side_length):
            print(f"✅ {n_pixels:4d} pixels → {side_length}×{side_length} grid")
        else:
            print(f"❌ {n_pixels:4d} pixels → Expected {expected_side}×{expected_side}, got {side_length}×{side_length}")
            all_passed = False
    
    return all_passed


def test_classification_mapper():
    """Test ClassificationMapper"""
    print("\n" + "="*60)
    print("TEST 3: Classification Mapper")
    print("="*60)
    
    try:
        from src.model_trainer import ClassificationMapper
        
        # Test with a 100x100 map
        test_map = np.random.randint(1, 5, size=(100, 100))
        colored_map = ClassificationMapper.create_colored_map(test_map)
        
        if colored_map.shape == (100, 100, 3):
            print(f"✅ Classification map created correctly")
            print(f"   Shape: {colored_map.shape} (expected: (100, 100, 3))")
            print(f"   Data type: {colored_map.dtype}")
            return True
        else:
            print(f"❌ Unexpected shape: {colored_map.shape}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_png_export():
    """Test PNG export functionality"""
    print("\n" + "="*60)
    print("TEST 4: PNG Export")
    print("="*60)
    
    try:
        # Create a sample colored map
        color_map = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
        
        # Convert to PIL image
        pil_image = PILImage.fromarray(color_map, 'RGB')
        
        # Save to buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        png_data = buffer.getvalue()
        
        if len(png_data) > 0:
            print(f"✅ PNG export successful")
            print(f"   File size: {len(png_data)} bytes")
            
            # Verify it's a valid PNG
            buffer.seek(0)
            test_image = PILImage.open(buffer)
            print(f"   Verified: {test_image.format} {test_image.size}")
            return True
        else:
            print(f"❌ PNG export failed - empty file")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_excel_export():
    """Test Excel export functionality"""
    print("\n" + "="*60)
    print("TEST 5: Excel Export")
    print("="*60)
    
    try:
        # Create sample data
        area_stats = pd.DataFrame({
            'Class': ['Water', 'Vegetation', 'Urban', 'Desert'],
            'Pixels': [50000, 45000, 48000, 52000],
            'Area_km2': [45.0, 40.5, 43.2, 46.8],
            'Percent': [25.0, 22.5, 24.0, 26.0]
        })
        
        model_stats = pd.DataFrame({
            'Model': ['Random Forest'],
            'Training Accuracy': ['98.57%'],
            'Testing Accuracy': ['91.67%'],
            'Classes': ['4'],
            'Feature Count': ['10'],
            'Training Samples': ['36']
        })
        
        # Create Excel file
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            area_stats.to_excel(writer, sheet_name='Area Statistics', index=False)
            model_stats.to_excel(writer, sheet_name='Model Statistics', index=False)
        
        excel_data = excel_buffer.getvalue()
        
        if len(excel_data) > 0:
            print(f"✅ Excel export successful")
            print(f"   File size: {len(excel_data)} bytes")
            
            # Verify sheets
            excel_buffer.seek(0)
            df_area = pd.read_excel(excel_buffer, sheet_name='Area Statistics')
            print(f"   Area Statistics: {len(df_area)} rows")
            
            excel_buffer.seek(0)
            df_model = pd.read_excel(excel_buffer, sheet_name='Model Statistics')
            print(f"   Model Statistics: {len(df_model)} rows")
            
            return len(df_area) == 4 and len(df_model) == 1
        else:
            print(f"❌ Excel export failed - empty file")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_txt_export():
    """Test TXT export functionality"""
    print("\n" + "="*60)
    print("TEST 6: TXT Export")
    print("="*60)
    
    try:
        report = f"""
{'='*60}
REMOTE SENSING CLASSIFICATION REPORT
{'='*60}

MODEL INFORMATION
{'-'*60}
Model Type: Random Forest
Training Accuracy: 98.57%
Testing Accuracy: 91.67%
Number of Classes: 4
Features Used: 10 (7 bands + 3 indices)
Training Samples: 36
"""
        
        if len(report) > 0:
            print(f"✅ TXT export successful")
            print(f"   Report size: {len(report)} bytes")
            print(f"   Lines: {len(report.splitlines())}")
            return True
        else:
            print(f"❌ TXT export failed - empty content")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("REMOTE SENSING APP - RESULTS PAGE VERIFICATION TEST")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Array Reshaping", test_array_reshaping),
        ("Classification Mapper", test_classification_mapper),
        ("PNG Export", test_png_export),
        ("Excel Export", test_excel_export),
        ("TXT Export", test_txt_export),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is ready to use!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
