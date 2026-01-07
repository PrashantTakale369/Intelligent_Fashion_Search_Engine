"""
Caption → normalized text logic

"""
from typing import List
from models.text_norm_model import TextNormalizationModel
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TextNormalizer:
    """Handle text normalization from captions"""
    
    def __init__(self, model: TextNormalizationModel):
        """Initialize text normalizer """
        self.model = model
    
    def process_single(self, caption: str) -> str:
        """
        Normalize single caption
        Returns: Normalized text
        """
        logger.info(f"Normalizing caption: {caption[:50]}...")
        normalized = self.model.normalize_text(caption)
        logger.debug(f"Normalized: {normalized}")
        return normalized
    
    def process_batch(self, captions: List[str]) -> List[str]:
        """
        Normalize batch of captions
        Returns:List of normalized texts
        """
        logger.info(f"Normalizing {len(captions)} captions")
        normalized_texts = self.model.normalize_texts_batch(captions)
        return normalized_texts
