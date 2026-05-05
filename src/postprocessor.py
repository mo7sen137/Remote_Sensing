"""
Map Generation and Post-Processing Module
Converts classifications to visual maps and calculates statistics
"""

import numpy as np
from PIL import Image
import pandas as pd
from typing import Dict, Tuple
import os

import config


class MapGenerator:
    """
    Generates classified maps and calculates area statistics.
    """
    
    def __init__(self, color_palette: Dict[str, Tuple] = None):
        """
        Initialize map generator with color palette.
        
        Args:
            color_palette: Dictionary mapping class names to RGB tuples
        """
        self.color_palette = color_palette or config.COLOR_PALETTE
        self.class_names = config.CLASS_NAMES
    
    def predictions_to_rgb(self, predictions: np.ndarray, 
                          height: int, width: int) -> np.ndarray:
        """
        Convert class predictions to RGB image array.
        
        Args:
            predictions: 1D array of class predictions (0-3)
            height: Image height
            width: Image width
            
        Returns:
            3D RGB array of shape (height, width, 3)
        """
        # Reshape predictions back to 2D
        pred_map = predictions.reshape(height, width)
        
        # Create RGB image (3 channels)
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Map predictions to colors
        for class_id, class_name in self.class_names.items():
            color = self.color_palette[class_name]
            mask = pred_map == class_id
            rgb_image[mask] = color
        
        return rgb_image
    
    def save_map(self, rgb_image: np.ndarray, output_path: str) -> None:
        """
        Save RGB image to file.
        
        Args:
            rgb_image: 3D RGB array
            output_path: Path to save image
        """
        img = Image.fromarray(rgb_image, 'RGB')
        img.save(output_path, quality=95)
        print(f"✓ Map saved: {output_path}")
    
    def calculate_areas(self, predictions: np.ndarray, 
                       height: int, width: int) -> pd.DataFrame:
        """
        Calculate area for each land cover class.
        
        Args:
            predictions: 1D array of predictions
            height: Image height
            width: Image width
            
        Returns:
            DataFrame with class names, pixel counts, and areas (km²)
        """
        pred_map = predictions.reshape(height, width)
        
        # Pixel area in km²
        pixel_area_km2 = config.KM_CONVERSION
        
        results = []
        total_pixels = height * width
        
        for class_id, class_name in self.class_names.items():
            pixel_count = np.sum(pred_map == class_id)
            area_km2 = pixel_count * pixel_area_km2
            percentage = (pixel_count / total_pixels) * 100
            
            results.append({
                'Class': class_name.capitalize(),
                'Pixels': int(pixel_count),
                'Area (km²)': f"{area_km2:.2f}",
                'Percentage (%)': f"{percentage:.2f}",
                'Color': config.HEX_COLORS[class_name]
            })
        
        df = pd.DataFrame(results)
        return df
    
    def save_statistics(self, statistics_df: pd.DataFrame, 
                       output_path: str) -> None:
        """
        Save statistics to CSV file.
        
        Args:
            statistics_df: DataFrame with statistics
            output_path: Path to save CSV
        """
        statistics_df.to_csv(output_path, index=False)
        print(f"✓ Statistics saved: {output_path}")
    
    @staticmethod
    def create_legend_image(color_palette: Dict[str, Tuple], 
                           output_path: str = None) -> Image.Image:
        """
        Create a legend image for the classification.
        
        Args:
            color_palette: Color mapping
            output_path: Optional path to save legend
            
        Returns:
            PIL Image object
        """
        # Create legend image (400x200)
        legend_img = Image.new('RGB', (400, 200), color='white')
        pixels = legend_img.load()
        
        # Simple text rendering (requires PIL ImageDraw - simplified here)
        # In a real app, use ImageDraw.ImageDraw for proper text
        
        if output_path:
            legend_img.save(output_path)
        
        return legend_img


class AccuracyAssessment:
    """
    Assess model accuracy against ground truth data.
    """
    
    @staticmethod
    def calculate_confusion_matrix(y_true: np.ndarray, 
                                   y_pred: np.ndarray,
                                   n_classes: int = 4) -> np.ndarray:
        """
        Calculate confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            n_classes: Number of classes
            
        Returns:
            Confusion matrix (n_classes × n_classes)
        """
        confusion = np.zeros((n_classes, n_classes), dtype=int)
        
        for true, pred in zip(y_true, y_pred):
            confusion[int(true), int(pred)] += 1
        
        return confusion
    
    @staticmethod
    def calculate_accuracy_metrics(confusion_matrix: np.ndarray) -> Dict:
        """
        Calculate accuracy metrics from confusion matrix.
        
        Args:
            confusion_matrix: Confusion matrix
            
        Returns:
            Dictionary with metrics (Accuracy, Precision, Recall, F1 per class)
        """
        n_classes = confusion_matrix.shape[0]
        metrics = {}
        
        # Overall Accuracy
        correct = np.trace(confusion_matrix)
        total = np.sum(confusion_matrix)
        metrics['Overall Accuracy'] = correct / total if total > 0 else 0
        
        # Per-class metrics
        for class_id in range(n_classes):
            tp = confusion_matrix[class_id, class_id]
            fp = np.sum(confusion_matrix[:, class_id]) - tp
            fn = np.sum(confusion_matrix[class_id, :]) - tp
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics[f'Class {class_id}'] = {
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1
            }
        
        return metrics
    
    @staticmethod
    def metrics_to_dataframe(metrics: Dict) -> pd.DataFrame:
        """
        Convert metrics dictionary to DataFrame for display.
        
        Args:
            metrics: Metrics dictionary
            
        Returns:
            DataFrame with metrics
        """
        rows = []
        
        for key, value in metrics.items():
            if isinstance(value, dict):
                for metric_name, score in value.items():
                    rows.append({
                        'Class': key,
                        'Metric': metric_name,
                        'Score': f"{score:.4f}"
                    })
        
        return pd.DataFrame(rows)
