"""
BAGE embedding wrapper for text to vector conversion
"""
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from typing import List
import numpy as np


class EmbeddingModel:
    """Wrapper for BAAI/bge-large-en-v1.5 model"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        """
        Initialize the embedding model
        device: Device to run model on (cuda/cpu)
        """
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
        self.model.to(device)
        self.model.eval()
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        Returns:Embedding vector as numpy array
        """
        # Tokenize
        encoded_input = self.tokenizer(
            text, 
            padding=True, 
            truncation=True, 
            max_length=512,
            return_tensors='pt'
        )
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        
        # Generate embedding
        with torch.no_grad():

            model_output = self.model(**encoded_input)
            # Use CLS token embedding (first token)
            embeddings = model_output[0][:, 0]
        
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        return embeddings.cpu().numpy()[0]
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        Returns: Array of embedding vectors
        """
        
        # Tokenize batch
        encoded_input = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        )
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        
        # Generate embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Use CLS token embedding (first token)
            embeddings = model_output[0][:, 0]
        
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        return embeddings.cpu().numpy()
