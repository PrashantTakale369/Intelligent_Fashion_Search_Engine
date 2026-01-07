"""
Image → caption logic
"""
from typing import List
from models.img_to_text_model import ImageToTextModel
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CaptionGenerator:

    """Handle caption generation from images"""
    
    def __init__(self, model: ImageToTextModel):
        """ Initialize caption generator """
        self.model = model
    
    def process_single(self, image_path: str) -> str:
        """ Generate caption for single image from image_path: Path to image
        Returns: Generated caption
        """
        logger.info(f"Generating caption for: {image_path}")
        caption = self.model.generate_caption(image_path)
        logger.debug(f"Caption: {caption}")
        return caption
    
    def process_batch(self, image_paths: List[str]) -> List[str]:
        """
        Generate captions for batch of images from image_paths: List of image paths
        Returns: List of generated captions
        """
        logger.info(f"Generating captions for {len(image_paths)} images")
        captions = self.model.generate_captions_batch(image_paths)
        return captions
