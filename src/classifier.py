"""
Land Classification Module
Handles model loading and prediction
"""

import numpy as np
import joblib
from typing import Dict, Tuple, Optional
import os


class LandClassifier:
    """
    Loads trained models and performs land cover classification.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize classifier with a trained model.
        
        Args:
            model_path: Path to trained model (.pkl or .joblib file)
        """
        self.model = None
        self.scaler = None
        self.model_name = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load trained model from disk.
        
        Args:
            model_path: Path to model file
            
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            self.model = joblib.load(model_path)
            self.model_name = os.path.basename(model_path).split('.')[0]
            print(f"✓ Model loaded: {self.model_name}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def load_scaler(self, scaler_path: str) -> None:
        """
        Load fitted scaler for feature normalization.
        
        Args:
            scaler_path: Path to scaler file
        """
        if os.path.exists(scaler_path):
            try:
                self.scaler = joblib.load(scaler_path)
                print(f"✓ Scaler loaded from {scaler_path}")
            except Exception as e:
                print(f"Warning: Could not load scaler: {str(e)}")
        else:
            print(f"Warning: Scaler file not found at {scaler_path}")
    
    def reshape_to_samples(self, feature_stack: np.ndarray) -> np.ndarray:
        """
        Reshape 3D feature stack to 2D samples array.
        
        Args:
            feature_stack: 3D array of shape (height, width, n_features)
            
        Returns:
            2D array of shape (n_samples, n_features)
        """
        height, width, n_features = feature_stack.shape
        samples = feature_stack.reshape(-1, n_features)
        return samples
    
    def normalize_features(self, samples: np.ndarray) -> np.ndarray:
        """
        Apply scaler normalization if available.
        
        Args:
            samples: 2D array of features
            
        Returns:
            Normalized samples
        """
        if self.scaler is not None:
            try:
                samples = self.scaler.transform(samples)
            except Exception as e:
                print(f"Warning: Could not apply scaler: {str(e)}")
        
        return samples
    
    def predict(self, feature_stack: np.ndarray) -> np.ndarray:
        """
        Classify all pixels in feature stack.
        
        Args:
            feature_stack: 3D array of shape (height, width, n_features)
            
        Returns:
            1D array of predicted class labels (0-3 for 4 classes)
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        height, width, n_features = feature_stack.shape
        
        # Reshape to 2D samples
        samples = self.reshape_to_samples(feature_stack)
        
        # Normalize if scaler available
        samples = self.normalize_features(samples)
        
        # Predict
        predictions = self.model.predict(samples)
        
        return predictions
    
    def predict_proba(self, feature_stack: np.ndarray) -> Optional[np.ndarray]:
        """
        Get prediction probabilities if model supports it.
        
        Args:
            feature_stack: 3D array of shape (height, width, n_features)
            
        Returns:
            2D array of probabilities or None if not supported
        """
        if self.model is None:
            raise ValueError("No model loaded.")
        
        if not hasattr(self.model, 'predict_proba'):
            return None
        
        height, width, n_features = feature_stack.shape
        samples = self.reshape_to_samples(feature_stack)
        samples = self.normalize_features(samples)
        
        probabilities = self.model.predict_proba(samples)
        return probabilities
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model metadata
        """
        if self.model is None:
            return {}
        
        info = {
            'name': self.model_name,
            'type': type(self.model).__name__,
            'supports_proba': hasattr(self.model, 'predict_proba'),
        }
        
        if hasattr(self.model, 'n_classes_'):
            info['n_classes'] = self.model.n_classes_
        
        return info


class MultiModelEnsemble:
    """
    Manages multiple classifiers for model comparison/ensemble.
    """
    
    def __init__(self, models_dir: str):
        """
        Initialize ensemble with models from directory.
        
        Args:
            models_dir: Directory containing trained model files
        """
        self.classifiers = {}
        self.models_dir = models_dir
        self.load_all_models()
    
    def load_all_models(self) -> None:
        """Load all .pkl and .joblib files from models directory."""
        if not os.path.exists(self.models_dir):
            print(f"Warning: Models directory not found: {self.models_dir}")
            return
        
        for filename in os.listdir(self.models_dir):
            if filename.endswith(('.pkl', '.joblib')):
                filepath = os.path.join(self.models_dir, filename)
                try:
                    classifier = LandClassifier(filepath)
                    model_name = filename.split('.')[0]
                    self.classifiers[model_name] = classifier
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
    
    def get_available_models(self) -> list:
        """Get list of available model names."""
        return list(self.classifiers.keys())
    
    def predict_with_model(self, model_name: str, feature_stack: np.ndarray) -> np.ndarray:
        """
        Predict using specific model.
        
        Args:
            model_name: Name of the model (without extension)
            feature_stack: 3D feature array
            
        Returns:
            Predictions array
        """
        if model_name not in self.classifiers:
            raise ValueError(f"Model {model_name} not found. Available: {self.get_available_models()}")
        
        return self.classifiers[model_name].predict(feature_stack)
    
    def ensemble_predict(self, feature_stack: np.ndarray, method: str = 'majority') -> np.ndarray:
        """
        Combine predictions from all models.
        
        Args:
            feature_stack: 3D feature array
            method: 'majority' for majority voting, 'mean' for mean probability
            
        Returns:
            Ensemble predictions
        """
        if not self.classifiers:
            raise ValueError("No models loaded in ensemble")
        
        if method == 'majority':
            # Majority voting
            all_predictions = []
            for classifier in self.classifiers.values():
                all_predictions.append(classifier.predict(feature_stack))
            
            all_predictions = np.array(all_predictions)
            # Get mode across models
            ensemble_pred = np.apply_along_axis(
                lambda x: np.bincount(x.astype(int)).argmax(),
                axis=0,
                arr=all_predictions
            )
            return ensemble_pred
        
        else:
            raise ValueError(f"Unknown ensemble method: {method}")
