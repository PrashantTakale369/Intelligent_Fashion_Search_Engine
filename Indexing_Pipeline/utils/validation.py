"""
Validation utilities
"""
import os
from typing import List
from pathlib import Path


def validate_image_path(image_path: str) -> bool:
    """Check if image path exists and is valid"""
    return os.path.exists(image_path) and os.path.isfile(image_path)


def validate_image_format(image_path: str, supported_formats: List[str]) -> bool:
    """Check if image has supported format"""
    ext = Path(image_path).suffix.lower()
    return ext in supported_formats


def validate_text(text: str) -> bool:
    """Check if text is valid (not empty)"""
    return text is not None and len(text.strip()) > 0


def validate_embedding(embedding) -> bool:
    """Check if embedding is valid"""
    return embedding is not None and len(embedding) > 0
