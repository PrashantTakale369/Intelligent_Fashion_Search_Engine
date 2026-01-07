"""
Query Normalization Logic
"""
import sys
import os
import importlib.util

# Import text norm model from indexing pipeline
indexing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Indexing_Pipeline'))
text_norm_path = os.path.join(indexing_dir, 'models', 'text_norm_model.py')

spec = importlib.util.spec_from_file_location("text_norm_model", text_norm_path)
text_norm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(text_norm_module)
TextNormalizationModel = text_norm_module.TextNormalizationModel

from typing import List


class QueryNormalizer:
    """Normalize user queries using text normalization model"""
    
    def __init__(self, model: TextNormalizationModel):
        """
        Initialize query normalizer
        
        Args:
            model: Text normalization model instance
        """
        self.model = model
    
    def normalize(self, query: str) -> str:
        """
        Normalize a single query
        
        Args:
            query: User query text
            
        Returns:
            Normalized query text
        """
        normalized_text = self.model.normalize_text(query)
        return normalized_text.strip()
