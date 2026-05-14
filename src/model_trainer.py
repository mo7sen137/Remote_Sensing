"""
Model Training and Prediction Module
Handles training multiple ML models and generating classification maps
"""

import numpy as np
import pandas as pd
import io
from typing import Dict, Tuple, Optional

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


class FeatureExtractor:
    """Extract spectral indices from satellite bands"""
    
    @staticmethod
    def calibrate_bands(bands_data, sun_angle=39.31701271, M=2e-5, A=-0.1):
        """
        Radiometric calibration of bands
        
        Args:
            bands_data: List of 7 band arrays
            sun_angle: Sun elevation angle in degrees
            M, A: Calibration coefficients
            
        Returns:
            List of calibrated band arrays
        """
        S = np.sin(np.deg2rad(sun_angle))
        B_cal = []
        
        for b in bands_data:
            calibrated = np.clip((M * b.astype(float) + A) / S, 0, 1)
            B_cal.append(calibrated)
        
        return B_cal
    
    @staticmethod
    def calculate_indices(B_cal):
        """
        Calculate spectral indices
        
        Args:
            B_cal: List of 7 calibrated bands
            
        Returns:
            Tuple of (NDVI, NDWI, NDBI)
        """
        e = 1e-10
        
        # NDVI = (NIR - Red) / (NIR + Red)
        NDVI = (B_cal[4] - B_cal[3]) / (B_cal[4] + B_cal[3] + e)
        
        # NDWI = (Green - NIR) / (Green + NIR)
        NDWI = (B_cal[2] - B_cal[4]) / (B_cal[2] + B_cal[4] + e)
        
        # NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
        NDBI = (B_cal[5] - B_cal[4]) / (B_cal[5] + B_cal[4] + e)
        
        # Handle NaN values
        NDVI[np.isnan(NDVI)] = 0
        NDWI[np.isnan(NDWI)] = 0
        NDBI[np.isnan(NDBI)] = 0
        
        return NDVI, NDWI, NDBI
    
    @staticmethod
    def create_feature_stack(B_cal, NDVI, NDWI, NDBI):
        """
        Stack bands and indices into feature array
        
        Args:
            B_cal: List of 7 calibrated bands
            NDVI, NDWI, NDBI: Spectral indices
            
        Returns:
            Feature stack of shape (height, width, 10)
        """
        features = np.dstack(B_cal + [NDVI, NDWI, NDBI])
        return features


class ModelTrainer:
    """Train multiple ML models on ROI data"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.statistics = {}
        self.train_data = None
        self.test_data = None
    
    def prepare_training_data(self, roi_df, B_cal, NDVI, NDWI, NDBI):
        """
        Prepare training data from ROI
        
        Args:
            roi_df: DataFrame with ROI samples (must have 'Class_Label' column)
            B_cal: List of 7 calibrated bands
            NDVI, NDWI, NDBI: Spectral indices
            
        Returns:
            X_train_n, X_test_n, Y_train, Y_test
        """
        # Calibrate ROI bands
        Br = [roi_df[f'B{i+1}'].values.astype(float) for i in range(7)]
        
        # Calculate indices for ROI
        e = 1e-10
        NDVI_r = (Br[4] - Br[3]) / (Br[4] + Br[3] + e)
        NDWI_r = (Br[2] - Br[4]) / (Br[2] + Br[4] + e)
        NDBI_r = (Br[5] - Br[4]) / (Br[5] + Br[4] + e)
        
        NDVI_r[np.isnan(NDVI_r)] = 0
        NDWI_r[np.isnan(NDWI_r)] = 0
        NDBI_r[np.isnan(NDBI_r)] = 0
        
        # Stack features
        X = np.column_stack(Br + [NDVI_r, NDWI_r, NDBI_r])
        Y = roi_df['Class_Label'].values
        
        # Split data
        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.3, random_state=self.random_state, stratify=Y
        )
        
        # Normalize
        X_train_n = self.scaler.fit_transform(X_train)
        X_test_n = self.scaler.transform(X_test)
        
        self.train_data = (X_train_n, X_test_n, Y_train, Y_test)
        
        return X_train_n, X_test_n, Y_train, Y_test
    
    def train_mlp(self, X_train_n, X_test_n, Y_train, Y_test, epochs=40):
        """
        Train MLP classifier with accuracy tracking
        
        Args:
            X_train_n, X_test_n: Normalized training/test data
            Y_train, Y_test: Training/test labels
            epochs: Number of training epochs
            
        Returns:
            Dict with trained model and history
        """
        mlp = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=1, warm_start=True)
        
        train_hist = []
        val_hist = []
        
        for epoch in range(epochs):
            mlp.fit(X_train_n, Y_train)
            
            train_acc = mlp.score(X_train_n, Y_train)
            val_acc = mlp.score(X_test_n, Y_test)
            
            train_hist.append(train_acc)
            val_hist.append(val_acc)
        
        self.models['MLP'] = mlp
        
        return {
            'model': mlp,
            'train_acc': train_hist[-1],
            'test_acc': val_hist[-1],
            'history': {'train': train_hist, 'val': val_hist}
        }
    
    def train_all_models(self, X_train, X_test, Y_train, Y_test):
        """
        Train all model types
        
        Args:
            X_train, X_test: Training/test data (already normalized if needed)
            Y_train, Y_test: Training/test labels
            
        Returns:
            Dict of all trained models
        """
        models_config = {
            'SVM': SVC(),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Tree': DecisionTreeClassifier(),
            'RF': RandomForestClassifier(n_estimators=50)
        }
        
        results = {}
        
        for name, model in models_config.items():
            model.fit(X_train, Y_train)
            
            train_acc = model.score(X_train, Y_train)
            test_acc = model.score(X_test, Y_test)
            
            self.models[name] = model
            results[name] = {
                'train_acc': train_acc,
                'test_acc': test_acc
            }
        
        return results
    
    def get_statistics_dataframe(self):
        """
        Get model statistics as DataFrame
        
        Returns:
            DataFrame with columns: Model, Training_Accuracy, Testing_Accuracy
        """
        stats = []
        
        for name, model in self.models.items():
            if self.train_data:
                X_train_n, X_test_n, Y_train, Y_test = self.train_data
                
                # Use normalized data for MLP
                if name == 'MLP':
                    tr = model.score(X_train_n, Y_train)
                    te = model.score(X_test_n, Y_test)
                else:
                    tr = model.score(X_train_n, Y_train)
                    te = model.score(X_test_n, Y_test)
            else:
                tr = te = 0
            
            stats.append([name, tr, te])
        
        return pd.DataFrame(stats, columns=['Model', 'Training_Accuracy', 'Testing_Accuracy'])


class ClassificationMapper:
    """Generate classification maps and statistics"""
    
    CLASS_NAMES = {1: 'Water', 2: 'Vegetation', 3: 'Urban', 4: 'Desert'}
    CLASS_COLORS = {
        1: [0, 0, 255],      # Water - Blue
        2: [0, 255, 0],      # Vegetation - Green
        3: [255, 0, 0],      # Urban - Red
        4: [255, 165, 0]     # Desert - Orange
    }
    
    @staticmethod
    def create_classification_map(features, model, rows, cols):
        """
        Create classification map from features
        
        Args:
            features: Feature stack of shape (height, width, n_features)
            model: Trained classifier
            rows, cols: Image dimensions
            
        Returns:
            Classification map
        """
        X_full = features.reshape(-1, features.shape[2])
        Y_pred = model.predict(X_full)
        class_map = Y_pred.reshape(rows, cols)
        
        return class_map
    
    @staticmethod
    def create_colored_map(class_map, no_data_mask=None):
        """
        Create RGB colored classification map
        
        Args:
            class_map: Classification map
            no_data_mask: Boolean mask for no-data pixels
            
        Returns:
            RGB image array
        """
        rows, cols = class_map.shape
        color_map = np.zeros((rows, cols, 3), dtype=np.float32)
        
        # Apply colors for each class
        for class_id, color in ClassificationMapper.CLASS_COLORS.items():
            mask = (class_map == class_id)
            color_map[mask] = color
        
        # Set no-data to black
        if no_data_mask is not None:
            color_map[no_data_mask] = 0
        
        return color_map
    
    @staticmethod
    def calculate_area_statistics(class_map, pixel_size_m=30):
        """
        Calculate area statistics for each class
        
        Args:
            class_map: Classification map
            pixel_size_m: Pixel size in meters (default 30m for Landsat)
            
        Returns:
            DataFrame with statistics
        """
        pixel_area_km2 = (pixel_size_m / 1000) ** 2
        total_pixels = class_map.size
        
        stats = []
        
        for class_id, class_name in ClassificationMapper.CLASS_NAMES.items():
            n_pixels = np.sum(class_map == class_id)
            area_km2 = n_pixels * pixel_area_km2
            percent = (n_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            
            stats.append({
                'Class': class_name,
                'Pixels': n_pixels,
                'Area_km2': area_km2,
                'Percent': percent
            })
        
        return pd.DataFrame(stats)
    
    @staticmethod
    def get_confusion_summary(Y_true, Y_pred):
        """
        Get simple classification summary
        
        Args:
            Y_true: True labels
            Y_pred: Predicted labels
            
        Returns:
            DataFrame with per-class accuracy
        """
        summary = []
        
        for class_id in range(1, 5):
            mask = Y_true == class_id
            if mask.sum() > 0:
                class_acc = (Y_pred[mask] == class_id).sum() / mask.sum()
                summary.append({
                    'Class': ClassificationMapper.CLASS_NAMES.get(class_id, f'Class_{class_id}'),
                    'Samples': mask.sum(),
                    'Accuracy': class_acc
                })
        
        return pd.DataFrame(summary)
