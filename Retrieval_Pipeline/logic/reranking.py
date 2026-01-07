"""
Reranking Logic using CLIP
"""
import os
import importlib.util
from typing import List, Tuple
import numpy as np

# Import CLIP model
current_dir = os.path.dirname(os.path.abspath(__file__))
clip_path = os.path.join(current_dir, '../models', 'clip_reranking_model.py')

spec = importlib.util.spec_from_file_location("clip_reranking_model", clip_path)
clip_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clip_module)
CLIPRerankingModel = clip_module.CLIPRerankingModel


class CLIPReranker:
    """Rerank search results using CLIP model"""
    
    def __init__(self, model: CLIPRerankingModel):
        """
        Initialize reranker
        
        Args:
            model: CLIP reranking model instance
        """
        self.model = model
    
    def rerank(self, query: str, image_paths: List[str], top_k: int = 10) -> Tuple[List[int], List[float]]:
        """
        Rerank images based on CLIP similarity
        
        Args:
            query: Original user query (not normalized)
            image_paths: List of image file paths
            top_k: Number of top results to return
            
        Returns:
            Tuple of (indices, scores) for top-k results
        """
        # Encode query
        text_embedding = self.model.encode_text([query])
        
        # Encode images
        image_embeddings = self.model.encode_images(image_paths)
        
        # Compute similarities
        scores = self.model.compute_similarity(text_embedding, image_embeddings)
        
        # Get top-k indices
        top_k = min(top_k, len(scores))
        top_indices = np.argsort(scores)[::-1][:top_k]
        top_scores = scores[top_indices]
        
        return top_indices.tolist(), top_scores.tolist()
