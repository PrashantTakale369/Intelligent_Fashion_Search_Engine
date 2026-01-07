"""
Batching utilities
"""
from typing import List, Iterator, TypeVar

T = TypeVar('T')


def create_batches(items: List[T], batch_size: int) -> Iterator[List[T]]:
    """
    Create batches from list of items
    
    Args:
        items: List of items to batch
        batch_size: Size of each batch
    
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
