"""
Load images, batching
"""

import os
import sys
from pathlib import Path
from typing import List

# Add parent directory to path for standalone execution

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.logger import setup_logger
from utils.validation import validate_image_path, validate_image_format



logger = setup_logger(__name__)


class DatasetLoader:
    
    """Handle dataset loading and batching"""

    def __init__(self, image_dir: str, supported_formats: List[str]):
        """ Initialize dataset loader """
        self.image_dir = image_dir
        self.supported_formats = supported_formats
        self.image_paths = []
    
    def load_images(self) -> List[str]:
        
        """ Load all valid images from directory and List of image file paths """
        
        logger.info(f" load img from {self.image_dir}")
        
        image_paths = []
        for file_path in Path(self.image_dir).rglob('*'):
            if file_path.is_file():
                str_path = str(file_path)
                
                # Validate
                if validate_image_path(str_path) and validate_image_format(str_path, self.supported_formats):
                    image_paths.append(str_path)
        
        self.image_paths = sorted(image_paths)
        logger.info(f"Found {len(self.image_paths)} valid images")
        return self.image_paths
    
    def get_image_count(self) -> int:
        """Get total number of images"""
        return len(self.image_paths)
    
    def get_image_paths(self) -> List[str]:
        """Get list of all image paths"""
        return self.image_paths


# Test when run directly
if __name__ == "__main__":
    import yaml
    
    # Load config
    config_path = os.path.join(parent_dir, 'config', 'indexing.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Test dataset loader
    loader = DatasetLoader(
        image_dir=config['dataset']['image_dir'],
        supported_formats=config['dataset']['supported_formats']
    )
    
    paths = loader.load_images()
    
    print("\n" + "=" * 60)
    print("DATASET LOADER TEST")
    print("=" * 60)
    print(f"Image directory: {config['dataset']['image_dir']}")
    print(f"Total images found: {len(paths)}")
    print(f"Supported formats: {config['dataset']['supported_formats']}")
    print("\nFirst 5 images:")
    for i, path in enumerate(paths[:5], 1):
        print(f"  {i}. {os.path.basename(path)}")
    print("=" * 60)
