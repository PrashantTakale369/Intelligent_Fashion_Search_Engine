"""
Store vectors + ids in FAISS
"""
import faiss
import numpy as np
from typing import List
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FAISSWriter:
    """Handle FAISS vector index operations"""
    
    def __init__(self, config: dict):
        """
        Initialize FAISS index
        
        Args:
            config: FAISS configuration dict
        """
        self.config = config
        self.index_path = config['index_path']
        self.embedding_dim = config.get('embedding_dim', 1024)
        self.normalize_vectors = config.get('normalize_vectors', True)
        self.index = None
        self.image_ids = []  # Store image_ids corresponding to vectors
    
    def create_index(self):
        """Create new FAISS index"""
        # Using IndexFlatIP (Inner Product) for cosine similarity
        # Vectors should be normalized for cosine similarity
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        logger.info(f"Created FAISS index with dimension {self.embedding_dim}")
    
    def load_index(self):
        """Load existing FAISS index"""
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                logger.info(f"Loaded FAISS index from {self.index_path}")
                
                # Load image_ids if exists
                ids_path = self.index_path.replace('.bin', '_ids.npy')
                if os.path.exists(ids_path):
                    self.image_ids = np.load(ids_path).tolist()
                    logger.info(f"Loaded {len(self.image_ids)} image IDs")
            except Exception as e:
                logger.error(f"Failed to load index: {e}")
                self.create_index()
        else:
            logger.info("No existing index found, creating new one")
            self.create_index()
    
    def add_vector(self, image_id: int, embedding: np.ndarray):
        """
        Add single vector to index
        
        Args:
            image_id: Database image_id
            embedding: Embedding vector
        """
        # Normalize if required
        if self.normalize_vectors:
            embedding = embedding / np.linalg.norm(embedding)
        
        # Add to index
        self.index.add(embedding.reshape(1, -1).astype('float32'))
        self.image_ids.append(image_id)
        logger.debug(f"Added vector for image_id {image_id}")
    
    def add_vectors_batch(self, image_ids: List[int], embeddings: np.ndarray):
        """
        Add batch of vectors to index
        
        Args:
            image_ids: List of database image_ids
            embeddings: Array of embedding vectors
        """
        # Normalize if required
        if self.normalize_vectors:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        self.image_ids.extend(image_ids)
        logger.info(f"Added {len(image_ids)} vectors to index")
    
    def save_index(self):
        """Save FAISS index to disk"""
        try:
            # Save index
            faiss.write_index(self.index, self.index_path)
            
            # Save image_ids
            ids_path = self.index_path.replace('.bin', '_ids.npy')
            np.save(ids_path, np.array(self.image_ids))
            
            logger.info(f"Saved FAISS index to {self.index_path}")
            logger.info(f"Index contains {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> tuple:
        """
        Search for k nearest neighbors
        
        Args:
            query_embedding: Query vector
            k: Number of results
        
        Returns:
            (distances, image_ids)
        """
        # Normalize if required
        if self.normalize_vectors:
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'), 
            k
        )
        
        # Map indices to image_ids
        result_image_ids = [self.image_ids[idx] for idx in indices[0]]
        
        return distances[0], result_image_ids
