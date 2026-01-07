"""
image_id ↔ image_path mapping
"""
from typing import Dict, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageRegistry:

    """Maintain mapping between image_id and image_path"""
    
    def __init__(self):
        """Initialize registry"""
        self.id_to_path: Dict[int, str] = {}
        self.path_to_id: Dict[str, int] = {}
    
    def register(self, image_id: int, image_path: str):
        """
        Register image_id and path mapping
        
        Args:
            image_id: Database image_id
            image_path: Path to image fil
        """
        self.id_to_path[image_id] = image_path
        self.path_to_id[image_path] = image_id
        logger.debug(f"Registered: {image_id} -> {image_path}")
    
    def register_batch(self, image_ids: list, image_paths: list):
        """
        Register batch of mappings
        Args:
            image_ids: List of database image_ids
            image_paths: List of image paths
            
        """
        for image_id, image_path in zip(image_ids, image_paths):
            self.register(image_id, image_path)
        logger.info(f"Registered {len(image_ids)} mappings")
    
    def get_path(self, image_id: int) -> Optional[str]:
        """Get image path by ID"""
        return self.id_to_path.get(image_id)
    
    def get_id(self, image_path: str) -> Optional[int]:
        """Get image ID by path"""
        return self.path_to_id.get(image_path)
    
    def get_count(self) -> int:
        """Get total number of registered images"""
        return len(self.id_to_path)
