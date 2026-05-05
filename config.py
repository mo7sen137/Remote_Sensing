"""
Configuration file for Remote Sensing Land Classification Web App
Contains color palettes, calibration parameters, and constants
"""

# Color Palette (RGB tuples) for classification
COLOR_PALETTE = {
    'water': (0, 0, 255),          # Blue
    'agriculture': (0, 255, 0),    # Green
    'urban': (255, 0, 0),          # Red
    'desert': (255, 255, 0),       # Yellow
}

# Hex codes for UI display
HEX_COLORS = {
    'water': '#0000FF',
    'agriculture': '#00FF00',
    'urban': '#FF0000',
    'desert': '#FFFF00',
}

# Class mapping
CLASS_NAMES = {
    0: 'water',
    1: 'agriculture',
    2: 'urban',
    3: 'desert',
}

# Landsat 8 Band Information
LANDSAT_BANDS = {
    1: 'Coastal/Aerosol (0.43 - 0.45 μm)',
    2: 'Blue (0.45 - 0.51 μm)',
    3: 'Green (0.53 - 0.59 μm)',
    4: 'Red (0.64 - 0.67 μm)',
    5: 'NIR (0.85 - 0.88 μm)',
    6: 'SWIR1 (1.57 - 1.65 μm)',
    7: 'SWIR2 (2.11 - 2.29 μm)',
}

# Spectral Indices Formulas
SPECTRAL_INDICES = {
    'NDVI': {
        'name': 'Normalized Difference Vegetation Index',
        'formula': '(NIR - Red) / (NIR + Red)',
        'description': 'Highlights vegetation/agriculture areas'
    },
    'NDWI': {
        'name': 'Normalized Difference Water Index',
        'formula': '(NIR - SWIR1) / (NIR + SWIR1)',
        'description': 'Highlights water bodies'
    },
    'NDBI': {
        'name': 'Normalized Difference Built-up Index',
        'formula': '(SWIR1 - NIR) / (SWIR1 + NIR)',
        'description': 'Highlights urban/built-up areas'
    },
}

# Minimum pixels per class for training
MIN_PIXELS_PER_CLASS = 500
TOTAL_TRAINING_PIXELS = 2000

# Classification models to support
SUPPORTED_MODELS = {
    'SVM': 'Support Vector Machine',
    'RandomForest': 'Random Forest Classifier',
    'KNN': 'K-Nearest Neighbors',
}

# Default model selection
DEFAULT_MODEL = 'RandomForest'

# Output settings
OUTPUT_DPI = 150
OUTPUT_FORMAT = 'PNG'

# Area calculation
PIXEL_SIZE_METERS = 30  # Landsat 8 pixel size in meters
KM_CONVERSION = PIXEL_SIZE_METERS ** 2 / (1000 ** 2)
