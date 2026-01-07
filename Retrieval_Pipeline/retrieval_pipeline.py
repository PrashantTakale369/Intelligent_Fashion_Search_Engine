"""

Main Retrieval Pipeline

Flow:
1. User Query → Text Normalization (Qwen2.5-0.5B-Instruct)
2. Normalized Query → Embedding (BAAI/bge-large-en-v1.5)
3. Embedding → FAISS Semantic Search → Top-N (20) Results
4. Top-N Images + Original Query → CLIP Reranking → Top-K (10) Final Results



"""
import yaml
import os
import sys
from typing import List, Dict
import importlib.util

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
indexing_dir = os.path.abspath(os.path.join(current_dir, '../Indexing_Pipeline'))

# Function to import module from file path
def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import models
clip_module = import_from_path("clip_reranking_model", os.path.join(current_dir, "models", "clip_reranking_model.py"))
CLIPRerankingModel = clip_module.CLIPRerankingModel

text_norm_module = import_from_path("text_norm_model", os.path.join(indexing_dir, "models", "text_norm_model.py"))
TextNormalizationModel = text_norm_module.TextNormalizationModel

embedding_module = import_from_path("embedding_model", os.path.join(indexing_dir, "models", "embedding_model.py"))
EmbeddingModel = embedding_module.EmbeddingModel

# Import logic
query_norm_module = import_from_path("query_normalization", os.path.join(current_dir, "logic", "query_normalization.py"))
QueryNormalizer = query_norm_module.QueryNormalizer

query_embed_module = import_from_path("query_embedding", os.path.join(current_dir, "logic", "query_embedding.py"))
QueryEmbedder = query_embed_module.QueryEmbedder

rerank_module = import_from_path("reranking", os.path.join(current_dir, "logic", "reranking.py"))
CLIPReranker = rerank_module.CLIPReranker

# Import storage
faiss_module = import_from_path("faiss_searcher", os.path.join(current_dir, "storage", "faiss_searcher.py"))
FAISSSearcher = faiss_module.FAISSSearcher

postgres_module = import_from_path("postgres_reader", os.path.join(current_dir, "storage", "postgres_reader.py"))
PostgresReader = postgres_module.PostgresReader

# Import utils
logger_module = import_from_path("logger", os.path.join(current_dir, "utils", "logger.py"))
setup_logger = logger_module.setup_logger

logger = setup_logger(__name__)


class RetrievalPipeline:
    """Complete retrieval pipeline for fashion search"""
    
    def __init__(self, config_path: str):
        """
        Initialize retrieval pipeline
        
        Args:
            config_path: Path to configuration file
        """
        # Load config
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        logger.info("=" * 80)
        logger.info("INITIALIZING RETRIEVAL PIPELINE")
        logger.info("=" * 80)
        
        # Initialize models
        logger.info("\nLoading Models...")
        
        self.text_norm_model = TextNormalizationModel(
            model_path=self.config['models']['text_normalization']['path'],
            device=self.config['models']['text_normalization']['device']
        )
        logger.info("✓ Text Normalization Model loaded")
        
        self.embedding_model = EmbeddingModel(
            model_path=self.config['models']['embedding']['path'],
            device=self.config['models']['embedding']['device']
        )
        logger.info("✓ Embedding Model loaded")
        
        self.clip_model = CLIPRerankingModel(
            model_path=self.config['models']['reranking']['path'],
            device=self.config['models']['reranking']['device']
        )
        logger.info("✓ CLIP Reranking Model loaded")
        
        # Initialize logic components
        self.query_normalizer = QueryNormalizer(self.text_norm_model)
        self.query_embedder = QueryEmbedder(self.embedding_model)
        self.reranker = CLIPReranker(self.clip_model)
        
        # Initialize storage
        logger.info("\nLoading Storage...")
        
        index_path = os.path.join(os.path.dirname(__file__), self.config['database']['faiss']['index_path'])
        ids_path = os.path.join(os.path.dirname(__file__), self.config['database']['faiss']['ids_path'])
        
        self.faiss_searcher = FAISSSearcher(index_path, ids_path)
        self.postgres_reader = PostgresReader(self.config['database']['postgres'])
        self.postgres_reader.connect()
        
        # Get search config
        self.top_n = self.config['search']['top_n']
        self.top_k = self.config['search']['top_k']
        self.dataset_dir = os.path.join(os.path.dirname(__file__), self.config['dataset']['image_dir'])
        
        logger.info("=" * 80)
        logger.info("✓ RETRIEVAL PIPELINE READY")
        logger.info("=" * 80)
    
    def search(self, query: str) -> List[Dict]:
        """
        Search for fashion images matching the query
        
        Args:
            query: User query (e.g., "A person in a bright yellow raincoat")
            
        Returns:
            List of result dictionaries with image info and scores
        """
        logger.info(f"\n{'=' * 80}")
        logger.info(f"PROCESSING QUERY: {query}")
        logger.info(f"{'=' * 80}\n")
        
        # STEP 1: Normalize query
        logger.info("STEP 1: Text Normalization")
        normalized_query = self.query_normalizer.normalize(query)
        logger.info(f"  Original: {query}")
        logger.info(f"  Normalized: {normalized_query}\n")
        
        # STEP 2: Generate embedding
        logger.info("STEP 2: Embedding Generation")
        query_embedding = self.query_embedder.embed(normalized_query)
        logger.info(f"  Embedding shape: {query_embedding.shape}\n")
        
        # STEP 3: Semantic search with FAISS
        logger.info(f"STEP 3: Semantic Search (Top-{self.top_n})")
        image_ids, semantic_scores = self.faiss_searcher.search(query_embedding, self.top_n)
        logger.info(f"  Found {len(image_ids)} results from FAISS\n")
        
        # Deduplicate: Keep best score for each image_id
        unique_results = {}
        for img_id, score in zip(image_ids, semantic_scores):
            if img_id not in unique_results or score > unique_results[img_id]:
                unique_results[img_id] = score
        
        # Sort by score and take top results
        sorted_results = sorted(unique_results.items(), key=lambda x: x[1], reverse=True)[:self.top_n]
        unique_ids = [img_id for img_id, _ in sorted_results]
        unique_scores = [score for _, score in sorted_results]
        
        # Get image metadata from PostgreSQL
        images = self.postgres_reader.get_images_by_ids(unique_ids)
        
        # Create image_id to metadata mapping
        id_to_image = {img['id']: img for img in images}
        
        # Build list with proper order and scores
        semantic_results = []
        for img_id, score in zip(unique_ids, unique_scores):
            if img_id in id_to_image:
                img_data = id_to_image[img_id]
                img_data['semantic_score'] = float(score)
                semantic_results.append(img_data)
        
        # STEP 4: Rerank with CLIP
        logger.info(f"STEP 4: CLIP Reranking (Top-{self.top_k})")
        
        # Get image paths - construct full absolute paths
        image_paths = []
        for img in semantic_results:
            # If path is already absolute, use it; otherwise join with dataset_dir
            img_path = img['image_path']
            if not os.path.isabs(img_path):
                img_path = os.path.join(self.dataset_dir, img_path)
            image_paths.append(img_path)
        
        # Rerank using original query (not normalized)
        rerank_indices, rerank_scores = self.reranker.rerank(query, image_paths, self.top_k)
        
        # Build final results
        final_results = []
        for idx, score in zip(rerank_indices, rerank_scores):
            result = semantic_results[idx].copy()
            result['clip_score'] = float(score)
            result['final_rank'] = len(final_results) + 1
            final_results.append(result)
        
        logger.info(f"  Reranked to {len(final_results)} final results\n")
        
        logger.info(f"{'=' * 80}")
        logger.info(f"✓ SEARCH COMPLETED - {len(final_results)} results returned")
        logger.info(f"{'=' * 80}\n")
        
        return final_results
    
    def close(self):
        """Close pipeline resources"""
        self.postgres_reader.close()


if __name__ == "__main__":
    # Test the pipeline
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'retrieval.yaml')
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
