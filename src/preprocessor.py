"""
Radiometric Calibration Module
Converts Digital Numbers (DN) to Top-of-Atmosphere (TOA) Reflectance
"""

import numpy as np
from typing import Dict, Tuple, List


class RadiometricCalibration:
    """
    Performs radiometric calibration on Landsat 8 Digital Numbers (DN).
    Converts DN values to TOA Reflectance using metadata from MTL file.
    """
    
    def __init__(self, mtl_metadata: Dict[str, float]):
        """
        Initialize calibration with MTL metadata.
        
        Args:
            mtl_metadata: Dictionary containing ML_L1 coefficients from MTL file
                         Must include: ML (Radiance Multiplicative), AL (Radiance Additive),
                         QCalMax, QCalMin for each band
        """
        self.mtl_metadata = mtl_metadata
        self.sun_elevation = mtl_metadata.get('SUN_ELEVATION_ANGLE', 45.0)
        
    def dn_to_toa_reflectance(self, dn_array: np.ndarray, band: int) -> np.ndarray:
        """
        Convert DN to TOA Reflectance.
        
        Formula:
            1. DN → Radiance: L = ML * (QCal + AL)
            2. Radiance → TOA Reflectance: ρ' = π * L / (ESUN * sin(θ))
            3. Apply Sun Angle Correction: ρ = ρ' / sin(θ)
        
        Args:
            dn_array: 2D numpy array of DN values
            band: Landsat 8 band number (2-7 for surface reflectance bands)
            
        Returns:
            2D numpy array of TOA Reflectance values (0-1 range)
        """
        # Radiance multiplicative and additive coefficients
        ml = self.mtl_metadata.get(f'ML_B{band}', 1.0)
        al = self.mtl_metadata.get(f'AL_B{band}', 0.0)
        
        # ESUN values for Landsat 8 (Watts/(m^2 * μm))
        esun_values = {
            2: 1895.3, 3: 1579.4, 4: 967.5, 5: 245.5, 6: 82.0, 7: 10.8
        }
        esun = esun_values.get(band, 1.0)
        
        # Convert DN to Radiance
        radiance = ml * dn_array + al
        
        # Sun angle correction
        sin_elevation = np.sin(np.radians(self.sun_elevation))
        
        # Calculate TOA Reflectance
        toa_reflectance = (np.pi * radiance) / (esun * sin_elevation)
        
        # Clip to valid range [0, 1]
        toa_reflectance = np.clip(toa_reflectance, 0, 1)
        
        return toa_reflectance
    
    def calibrate_bands(self, bands_dict: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
        """
        Calibrate all provided bands.
        
        Args:
            bands_dict: Dictionary with band numbers as keys and DN arrays as values
            
        Returns:
            Dictionary with same band numbers and calibrated reflectance arrays
        """
        calibrated_bands = {}
        
        for band_num, dn_array in bands_dict.items():
            calibrated_bands[band_num] = self.dn_to_toa_reflectance(dn_array, band_num)
            
        return calibrated_bands
    
    @staticmethod
    def parse_mtl_file(mtl_path: str) -> Dict[str, float]:
        """
        Parse Landsat 8 MTL metadata file.
        
        Args:
            mtl_path: Path to MTL_L1.txt file
            
        Returns:
            Dictionary of metadata key-value pairs
        """
        metadata = {}
        
        try:
            with open(mtl_path, 'r') as f:
                content = f.read()
                
            # Extract key-value pairs
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('GROUP'):
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip().strip('"')
                    
                    try:
                        # Try to convert to float
                        metadata[key] = float(value)
                    except ValueError:
                        # Keep as string if not numeric
                        metadata[key] = value
                        
        except FileNotFoundError:
            print(f"Warning: MTL file not found at {mtl_path}")
            
        return metadata
