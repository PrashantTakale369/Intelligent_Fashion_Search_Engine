"""
FAISS Vector Search
"""
import faiss
import numpy as np
from typing import List, Tuple
import os


class FAISSSearcher:
    """FAISS searcher for semantic similarity search"""
    
    def __init__(self, index_path: str, ids_path: str):
        """
        Initialize FAISS searcher
        
        Args:
            index_path: Path to FAISS index file
            ids_path: Path to image IDs numpy file
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        
        if not os.path.exists(ids_path):
            raise FileNotFoundError(f"Image IDs file not found at {ids_path}")
        
        print(f"Loading FAISS index from {index_path}...")
        self.index = faiss.read_index(index_path)
        self.image_ids = np.load(ids_path, allow_pickle=True)
        
        print(f"✓ Loaded FAISS index with {self.index.ntotal} vectors")
        print(f"✓ Loaded {len(self.image_ids)} image IDs")
    
    def search(self, query_embedding: np.ndarray, top_n: int = 20) -> Tuple[List[int], List[float]]:
        """
        Search for similar images
        
        Args:
            query_embedding: Query embedding vector (1, dim)
            top_n: Number of top results to return
            
        Returns:
            Tuple of (image_ids, similarity_scores)
        """
        # Ensure query is 2D array
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Ensure float32
        query_embedding = query_embedding.astype('float32')
        
        # Search
        scores, indices = self.index.search(query_embedding, top_n)
        
        # Get image IDs
        result_ids = [int(self.image_ids[idx]) for idx in indices[0]]
        result_scores = scores[0].tolist()
        
        return result_ids, result_scores
