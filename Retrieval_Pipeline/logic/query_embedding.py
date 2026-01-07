"""
Query Embedding Logic
"""
import sys
import os
import importlib.util
import numpy as np

# Import embedding model from indexing pipeline
indexing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Indexing_Pipeline'))
embedding_path = os.path.join(indexing_dir, 'models', 'embedding_model.py')

spec = importlib.util.spec_from_file_location("embedding_model", embedding_path)
embedding_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(embedding_module)
EmbeddingModel = embedding_module.EmbeddingModel


class QueryEmbedder:
    """Generate embeddings for normalized queries"""
    
    def __init__(self, model: EmbeddingModel):
        """
        Initialize query embedder
        
        Args:
            model: Embedding model instance
        """
        self.model = model
    
    def embed(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        
        Args:
            query: Normalized query text
            
        Returns:
            Query embedding vector
        """
        embedding = self.model.generate_embedding(query)
        return embedding
