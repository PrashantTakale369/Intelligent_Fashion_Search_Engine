"""
Run Retrieval Pipeline Test
"""
import sys
import os

# Add paths before any imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import and run
from retrieval_pipeline import RetrievalPipeline

if __name__ == "__main__":
    config_path = os.path.join(current_dir, 'config', 'retrieval.yaml')
    pipeline = RetrievalPipeline(config_path)
    
    # Test query
    test_query = "A person in a bright yellow raincoat"
    results = pipeline.search(test_query)
    
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Image ID: {result['id']}")
        print(f"   Path: {result['image_path']}")
        print(f"   Semantic Score: {result['semantic_score']:.4f}")
        print(f"   CLIP Score: {result['clip_score']:.4f}")
    
    pipeline.close()
