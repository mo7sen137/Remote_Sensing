# 🛰️ Remote Sensing Land Classification Web Application

## Project Overview

This project implements an automated **Land Cover Classification System** using satellite imagery from Landsat 8. The system applies machine learning algorithms to classify pixels in satellite images into four categories:

- **💧 Water** (lakes, rivers, seas)
- **🌱 Agriculture** (crops, vegetation)
- **🏢 Urban** (buildings, streets, infrastructure)
- **🏜️ Desert** (bare soil, sand)

The solution features a professional **Streamlit-based web dashboard** for interactive classification and area computation.

---

## 📋 Project Requirements

### Dataset
- **Source**: USGS Earth Explorer (Landsat 8)
- **Location**: Path 177 / Row 039 (Nile Delta, Egypt)
- **Season**: Winter (minimal cloud cover)
- **Size**: 2000×2000 pixels (30m resolution = 60km×60km area)
- **Bands**: 7 reflectance bands (Bands 2-7)

### Machine Learning Pipeline
1. **Radiometric Calibration**: DN → TOA Reflectance
2. **Feature Extraction**: Calculate NDVI, NDWI, NDBI indices
3. **Classification**: Train & test 3+ ML models (SVM, Random Forest, KNN)
4. **Map Generation**: Produce colored classification map
5. **Area Statistics**: Calculate coverage per class

### Deliverables
- ✅ Python source code (modular, documented)
- ✅ Trained models (.pkl/.joblib files)
- ✅ Streamlit web application
- ✅ Classification map (PNG image)
- ✅ Area statistics (CSV file)
- ✅ PDF report
- ✅ Presentation slides

### Grading (20 points + 3 bonus)
- Code Implementation: 3 points
- Model Application: 5 points
- Generated Map: 2 points
- Report: 5 points
- Presentation: 5 points
- **Bonus**: Web Application with interactive features: 3 points

---

## 📁 Project Structure

```
Remote_Sensing/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration (colors, parameters)
│
├── src/                               # Core Processing Library
│   ├── __init__.py
│   ├── preprocessor.py               # Radiometric calibration (DN → Reflectance)
│   ├── feature_extractor.py          # NDVI, NDWI, NDBI calculation
│   ├── classifier.py                 # ML model loading & prediction
│   ├── postprocessor.py              # Map generation & area computation
│   └── utils.py                      # Utility functions (file I/O, validation)
│
├── app/                               # Streamlit Web Application
│   ├── __init__.py
│   ├── main.py                       # Entry point (streamlit run app/main.py)
│   ├── components.py                 # UI components (sidebar, tabs)
│   └── callbacks.py                  # Event handlers & processing logic
│
├── models/                            # Trained ML Models
│   ├── svm_model.pkl                 # SVM classifier (from team)
│   ├── rf_model.pkl                  # Random Forest classifier (from team)
│   ├── knn_model.pkl                 # KNN classifier (from team)
│   └── scaler.pkl                    # Feature scaler (StandardScaler)
│
├── data/                              # Data Storage
│   ├── sample_landsat/               # Example Landsat files (for testing)
│   ├── outputs/                      # Generated results
│   │   ├── classification_map.png
│   │   ├── area_statistics.csv
│   │   └── accuracy_metrics.json
│   └── mtl_example.txt               # Example MTL metadata
│
├── tests/                             # Unit Tests
│   ├── test_preprocessor.py          # Test calibration
│   ├── test_features.py              # Test indices extraction
│   └── test_classifier.py            # Test classification
│
└── notebooks/                         # Development & Exploration
    └── development.ipynb             # Jupyter notebook for experimentation
```

---

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Remote_Sensing
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Web Application

```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

### Running Tests

```bash
python -m pytest tests/ -v
```

---

## 📊 Pipeline Workflow

### Step 1: Data Loading
- Load 7 GeoTIFF files (Bands 2-7)
- Load MTL metadata file
- Validate band dimensions

### Step 2: Radiometric Calibration
```
Reflectance = π × Radiance / (ESUN × sin(θ))
```

### Step 3: Spectral Indices Calculation
```
NDVI = (NIR - Red) / (NIR + Red)        # Vegetation
NDWI = (NIR - SWIR1) / (NIR + SWIR1)    # Water
NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)    # Urban areas
```

### Step 4: Feature Stack Creation
- Stack: [B2, B3, B4, B5, B6, B7, NDVI, NDWI, NDBI, Reserved]
- Shape: (2000, 2000, 10)

### Step 5: Classification
- Reshape to 2D: (4M rows, 10 features)
- Apply trained model
- Get class predictions for each pixel

### Step 6: Map Generation
- Color-code pixels by class
- RGB output: Blue (Water), Green (Agriculture), Red (Urban), Yellow (Desert)

### Step 7: Area Computation
```
Area (km²) = Pixel_Count × (30 meters)² / (1000)²
```

---

## 🤖 Machine Learning Models

Three classifiers are trained on ground truth data:

| Model | Features | Advantages | Expected Accuracy |
|-------|----------|------------|-------------------|
| **SVM** | Linear/RBF kernel | Robust, handles high-dimensional data | 85-90% |
| **Random Forest** | Ensemble of trees | Fast prediction, interpretable | 88-93% |
| **KNN** | Distance-based | Simple, no training phase | 82-88% |

**Training Data**: 2000 pixels manually labeled in ENVI (500 each class)
**Test Data**: 30% of labeled pixels
**Target Accuracy**: >90% for bonus points

---

## 📦 Key Dependencies

```
streamlit           # Web dashboard
numpy              # Numerical computing
pandas             # Data manipulation
scikit-learn       # Machine learning
rasterio           # GeoTIFF file I/O
pillow             # Image processing
matplotlib         # Visualization
plotly             # Interactive charts
opencv-python      # Computer vision utilities
```

---

## 🎯 Implementation Checklist

**Phase 1: Core Engine** (Days 2-3)
- [x] Radiometric calibration module
- [x] Spectral indices extraction
- [x] Classification inference engine
- [x] Map generation & area calculation
- [x] Unit tests

**Phase 2: Web Interface** (Days 4-5)
- [x] Streamlit app structure
- [x] File upload handlers
- [x] Interactive tabs
- [x] Real-time preview
- [x] Result visualization

**Phase 3: Polish & Deploy** (Days 6-7)
- [ ] Full integration testing
- [ ] Performance optimization
- [ ] Error handling & validation
- [ ] Documentation
- [ ] Deployment preparation

---

## 📥 Input Files Format

### Landsat GeoTIFF Bands
- Format: GeoTIFF (.tif, .tiff)
- Naming: `LC08_L1TP_177039_20XX01XX_XXX_XX_B#_B*.TIF`
- Data Type: `uint16` (0-65535 DN values)
- Resolution: 30 meters/pixel

### Metadata File (MTL)
- Format: Text (.txt)
- Source: Included with Landsat download
- Contains: Radiometric rescaling coefficients (ML, AL)

---

## 📤 Output Files

### Classification Map
- **Format**: PNG image
- **Size**: 2000×2000 pixels
- **Color Coding**: 
  - Blue (RGB: 0,0,255) - Water
  - Green (RGB: 0,255,0) - Agriculture
  - Red (RGB: 255,0,0) - Urban
  - Yellow (RGB: 255,255,0) - Desert

### Area Statistics
- **Format**: CSV file
- **Columns**: Class, Pixel_Count, Area_km2, Percentage

### Model Accuracy Report
- **Format**: JSON
- **Metrics**: Overall accuracy, per-class precision/recall/F1

---

## 🔧 Configuration

Edit `config.py` to customize:
- Color palettes
- Class definitions
- Model paths
- Output parameters

---

## 📝 Submission

**Deadline**: May 14, 2026
**Format**: ZIP file containing:
1. Complete source code
2. Trained models
3. Generated maps & statistics
4. PDF report
5. Presentation slides

---

**Status**: 🟡 In Active Development
**Last Updated**: May 5, 2026