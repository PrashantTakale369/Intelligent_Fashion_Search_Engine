"""
Text → embedding logic
"""
from typing import List
import numpy as np
from models.embedding_model import EmbeddingModel
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingGenerator:
    """Handle embedding generation from normalized text"""
    
    def __init__(self, model: EmbeddingModel):
        """ Initialize embedding generator"""
        self.model = model
    
    def process_single(self, text: str) -> np.ndarray:
        
        """Generate embedding for single text text: Normalized text
        Returns:Embedding vector
        """
        logger.info(f"Generating embedding for: {text[:50]}...")
        embedding = self.model.generate_embedding(text)
        logger.debug(f"Embedding shape: {embedding.shape}")
        return embedding
    
    def process_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for batch of texts texts: List of normalized texts
        Returns:Array of embedding vectors
        """
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.generate_embeddings_batch(texts)
        logger.debug(f"Embeddings shape: {embeddings.shape}")
        return embeddings
