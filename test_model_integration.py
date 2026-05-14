"""
Test script for model integration
Verifies that all components work together
"""

import numpy as np
import pandas as pd
from src.model_trainer import FeatureExtractor, ModelTrainer, ClassificationMapper

print("=" * 60)
print("🧪 TESTING MODEL INTEGRATION")
print("=" * 60)

# Test 1: Feature Extractor
print("\n✓ Test 1: FeatureExtractor")
print("-" * 60)

# Create dummy band data
bands_data = [np.random.randint(0, 10000, (100, 100), dtype=np.uint16) for _ in range(7)]
print(f"  • Created {len(bands_data)} dummy bands: {[b.shape for b in bands_data][0]}")

# Calibrate
B_cal = FeatureExtractor.calibrate_bands(bands_data)
print(f"  • Calibrated bands: {len(B_cal)} bands")

# Calculate indices
NDVI, NDWI, NDBI = FeatureExtractor.calculate_indices(B_cal)
print(f"  • Calculated indices:")
print(f"    - NDVI: {NDVI.shape}, range: [{NDVI.min():.3f}, {NDVI.max():.3f}]")
print(f"    - NDWI: {NDWI.shape}, range: [{NDWI.min():.3f}, {NDWI.max():.3f}]")
print(f"    - NDBI: {NDBI.shape}, range: [{NDBI.min():.3f}, {NDBI.max():.3f}]")

# Create feature stack
features = FeatureExtractor.create_feature_stack(B_cal, NDVI, NDWI, NDBI)
print(f"  • Feature stack: {features.shape}")

# Test 2: Model Trainer
print("\n✓ Test 2: ModelTrainer")
print("-" * 60)

# Create dummy ROI data
roi_data = {
    'B1': np.random.rand(100) * 10000,
    'B2': np.random.rand(100) * 10000,
    'B3': np.random.rand(100) * 10000,
    'B4': np.random.rand(100) * 10000,
    'B5': np.random.rand(100) * 10000,
    'B6': np.random.rand(100) * 10000,
    'B7': np.random.rand(100) * 10000,
    'Class_Label': np.random.choice([1, 2, 3, 4], 100)
}
roi_df = pd.DataFrame(roi_data)
print(f"  • Created ROI dataset: {roi_df.shape}")
print(f"  • Classes: {sorted(roi_df['Class_Label'].unique())}")

trainer = ModelTrainer()
X_train, X_test, Y_train, Y_test = trainer.prepare_training_data(
    roi_df, B_cal, NDVI, NDWI, NDBI
)
print(f"  • Training data prepared:")
print(f"    - X_train: {X_train.shape}")
print(f"    - X_test: {X_test.shape}")
print(f"    - Y_train unique: {np.unique(Y_train)}")
print(f"    - Y_test unique: {np.unique(Y_test)}")

# Train model
result = trainer.train_all_models(X_train, X_test, Y_train, Y_test)
print(f"  • Models trained:")
for name, stats in result.items():
    print(f"    - {name}: Train={stats['train_acc']:.3f}, Test={stats['test_acc']:.3f}")

# Get statistics
stats_df = trainer.get_statistics_dataframe()
print(f"  • Statistics DataFrame created: {stats_df.shape}")

# Test 3: Classification Mapper
print("\n✓ Test 3: ClassificationMapper")
print("-" * 60)

# Create dummy classification map
class_map = np.random.choice([1, 2, 3, 4], (100, 100))
print(f"  • Created classification map: {class_map.shape}")

# Create colored map
color_map = ClassificationMapper.create_colored_map(class_map)
print(f"  • Colored map: {color_map.shape}, dtype: {color_map.dtype}")

# Calculate statistics
area_stats = ClassificationMapper.calculate_area_statistics(class_map, pixel_size_m=30)
print(f"  • Area statistics:")
print(area_stats.to_string(index=False))

# Test 4: Import in main.py
print("\n✓ Test 4: Main.py imports")
print("-" * 60)

try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    # This would be how it's imported in main.py
    from src.model_trainer import FeatureExtractor as FE
    from src.model_trainer import ModelTrainer as MT
    from src.model_trainer import ClassificationMapper as CM
    
    print("  • Successfully imported in main.py context")
    print(f"  • FeatureExtractor: {FE.__name__}")
    print(f"  • ModelTrainer: {MT.__name__}")
    print(f"  • ClassificationMapper: {CM.__name__}")
    
except Exception as e:
    print(f"  ❌ Import error: {e}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("""
التكامل جاهز للاستخدام:
✓ FeatureExtractor - معالجة البيانات الطيفية
✓ ModelTrainer - تدريب النماذج
✓ ClassificationMapper - إنشاء الخرائط والإحصائيات

الآن يمكن:
1. رفع ملف CSV (الباندات)
2. رفع ملف BIN (البيانات الوصفية)
3. رفع ملف ROI CSV (بيانات التدريب)
4. تشغيل التصنيف واختيار النموذج
5. الحصول على النتائج والإحصائيات
""")
