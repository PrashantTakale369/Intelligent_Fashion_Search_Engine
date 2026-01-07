"""
CLIP Model for Image-Text Reranking
"""
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from typing import List
import numpy as np


class CLIPRerankingModel:
    """CLIP model wrapper for reranking images based on text query"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        """
        Initialize CLIP model
        
        Args:
            model_path: Path or name of CLIP model
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
        
        print(f"Loading CLIP model on {self.device}...")
        self.model = CLIPModel.from_pretrained(model_path).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_path)
        self.model.eval()
        
    def encode_text(self, texts: List[str]) -> np.ndarray:
        """
        Encode text queries into embeddings
        
        Args:
            texts: List of text queries
            
        Returns:
            Text embeddings as numpy array
        """
        with torch.no_grad():
            inputs = self.processor(text=texts, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            text_features = self.model.get_text_features(**inputs)
            # Normalize features
            text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
            return text_features.cpu().numpy()
    
    def encode_images(self, image_paths: List[str]) -> np.ndarray:
        """
        Encode images into embeddings
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            Image embeddings as numpy array
        """
        images = [Image.open(img_path).convert("RGB") for img_path in image_paths]
        
        with torch.no_grad():
            inputs = self.processor(images=images, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            image_features = self.model.get_image_features(**inputs)
            # Normalize features
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
            return image_features.cpu().numpy()
    
    def compute_similarity(self, text_embeddings: np.ndarray, image_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute similarity scores between text and images
        
        Args:
            text_embeddings: Text embeddings (1, dim)
            image_embeddings: Image embeddings (N, dim)
            
        Returns:
            Similarity scores (N,)
        """
        # Compute cosine similarity (dot product of normalized vectors)
        scores = np.dot(text_embeddings, image_embeddings.T).squeeze()
        return scores
