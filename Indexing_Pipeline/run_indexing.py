"""
Entry point for indexing pipeline

Pipeline Flow is like this way : 

1. Load images from Dataset folder
2. Image Caption (Qwen2-VL-2B-Instruct) model we are used 
3. Caption Normalized Text (Qwen2.5-0.5B-Instruct) model we are used 
4. Store (image_id, path, normalized_text) in PostgreSQL
5. Normalized Text → Embedding (BAAI/bge-large-en-v1.5) model we are used 
6. Store (image_id, embedding) in FAISS


"""

import yaml
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Models
from models.img_to_text_model import ImageToTextModel
from models.text_norm_model import TextNormalizationModel
from models.embedding_model import EmbeddingModel

# Logic
from logic.caption_logic import CaptionGenerator
from logic.normalization_logic import TextNormalizer
from logic.embedding_logic import EmbeddingGenerator

# Storage
from storage.postgres_writer import PostgresWriter
from storage.faiss_writer import FAISSWriter

# Data
from data.dataset_loader import DatasetLoader
from data.image_registry import ImageRegistry

# Utils
from utils.logger import setup_logger
from utils.batching import create_batches

logger = setup_logger(__name__)


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    """Main indexing pipeline orchestrator"""
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'indexing.yaml')
    config = load_config(config_path)
    logger.info("Configuration loaded")
    
    # Initialize dataset loader
    logger.info("=" * 80)
    logger.info("STEP 1: Loading Dataset")
    logger.info("=" * 80)
    
    dataset_loader = DatasetLoader(
        image_dir=config['dataset']['image_dir'],
        supported_formats=config['dataset']['supported_formats']
    )
    image_paths = dataset_loader.load_images()
    
    if len(image_paths) == 0:
        logger.error("No images found in dataset!")
        return
    
    # Initialize models
    logger.info("=" * 80)
    logger.info("STEP 2: Loading Models")
    logger.info("=" * 80)
    
    img_to_text_model = ImageToTextModel(
        model_path=config['models']['img_to_text']['path'],
        device=config['models']['img_to_text']['device']
    )
    logger.info("✓ Image-to-Text model loaded")
    
    text_norm_model = TextNormalizationModel(
        model_path=config['models']['text_normalization']['path'],
        device=config['models']['text_normalization']['device']
    )
    logger.info("✓ Text Normalization model loaded")
    
    embedding_model = EmbeddingModel(
        model_path=config['models']['embedding']['path'],
        device=config['models']['embedding']['device']
    )
    logger.info("✓ Embedding model loaded")
    
    # Initialize logic processors
    caption_gen = CaptionGenerator(img_to_text_model)
    text_normalizer = TextNormalizer(text_norm_model)
    embedding_gen = EmbeddingGenerator(embedding_model)
    
    # Initialize storage
    logger.info("=" * 80)
    logger.info("STEP 3: Initializing Storage")
    logger.info("=" * 80)
    
    postgres = PostgresWriter(config['database']['postgres'])
    postgres.connect()
    
    # Create table if not exists
    schema_path = os.path.join(os.path.dirname(__file__), 'storage', 'schema.sql')
    postgres.create_table(schema_path)
    
    # Get already processed images
    processed_paths = set(postgres.get_all_image_paths())
    logger.info(f"Found {len(processed_paths)} already processed images")
    
    # Filter out already processed images
    unprocessed_images = [img for img in image_paths if img not in processed_paths]
    logger.info(f"Images to process: {len(unprocessed_images)}/{len(image_paths)}")
    
    if len(unprocessed_images) == 0:
        logger.info("All images already processed!")
        postgres.close()
        return
    
    faiss_writer = FAISSWriter(config['database']['faiss'])
    faiss_writer.load_index()
    
    # Initialize registry
    image_registry = ImageRegistry()
    
    # Process images in batches
    logger.info("=" * 80)
    logger.info("STEP 4: Processing Images")
    logger.info("=" * 80)
    
    batch_size = config['dataset']['batch_size']
    save_interval = config['processing']['save_interval']
    total_processed = 0
    
    for batch_idx, image_batch in enumerate(create_batches(unprocessed_images, batch_size)):
        logger.info(f"\n--- Batch {batch_idx + 1} ({len(image_batch)} images) ---")
        
        # Step 1: Image → Caption
        captions = caption_gen.process_batch(image_batch)
        
        # Step 2: Caption → Normalized Text
        normalized_texts = text_normalizer.process_batch(captions)
        
        # Step 3: Store in PostgreSQL
        records = list(zip(image_batch, normalized_texts))
        image_ids = postgres.insert_batch(records)
        
        # Register mappings
        image_registry.register_batch(image_ids, image_batch)
        
        # Step 4: Generate Embeddings
        embeddings = embedding_gen.process_batch(normalized_texts)
        
        # Step 5: Store in FAISS
        faiss_writer.add_vectors_batch(image_ids, embeddings)
        
        total_processed += len(image_batch)
        logger.info(f"✓ Processed {total_processed}/{len(unprocessed_images)} images")
        
        # Save FAISS index periodically
        if total_processed % save_interval == 0:
            faiss_writer.save_index()
            logger.info("✓ FAISS index saved (periodic)")
    
    # Final save
    logger.info("=" * 80)
    logger.info("STEP 5: Finalizing")
    logger.info("=" * 80)
    
    faiss_writer.save_index()
    postgres.close()
    
    logger.info("=" * 80)
    logger.info("INDEXING PIPELINE COMPLETED!")
    logger.info(f"Total images processed: {total_processed}")
    logger.info(f"FAISS index size: {faiss_writer.index.ntotal} vectors")
    logger.info(f"Registry size: {image_registry.get_count()} mappings")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
