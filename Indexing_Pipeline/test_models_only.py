"""
Test models without database - just to verify models are working
"""
import yaml
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from models.img_to_text_model import ImageToTextModel
from models.text_norm_model import TextNormalizationModel
from models.embedding_model import EmbeddingModel
from logic.caption_logic import CaptionGenerator
from logic.normalization_logic import TextNormalizer
from logic.embedding_logic import EmbeddingGenerator
from data.dataset_loader import DatasetLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'indexing.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Load one test image
    dataset_loader = DatasetLoader(
        image_dir=config['dataset']['image_dir'],
        supported_formats=config['dataset']['supported_formats']
    )
    image_paths = dataset_loader.load_images()
    
    if len(image_paths) == 0:
        logger.error("No images found!")
        return
    
    test_image = image_paths[0]
    logger.info(f"\n Test image: {test_image}")
    
    # Load models
    logger.info("\n")
    print("Loading Models...\n")
    
    img_to_text_model = ImageToTextModel(
        model_path=config['models']['img_to_text']['path'],
        device=config['models']['img_to_text']['device']
    )
    logger.info("\n")
    logger.info(" Your Image-to-Text model loaded Correctly \n")
    
    text_norm_model = TextNormalizationModel(
        model_path=config['models']['text_normalization']['path'],
        device=config['models']['text_normalization']['device']
    )
    logger.info("\n")
    logger.info(" Your Text Normalization model loaded Correctly \n")
    
    embedding_model = EmbeddingModel(
        model_path=config['models']['embedding']['path'],
        device=config['models']['embedding']['device']
    )
    logger.info("\n")
    logger.info(" Your Embedding model loaded Correctly \n")
    
    # Test pipeline
    logger.info("\n" + "=" * 80)
    logger.info("Testing Pipeline...\n")
    
    # Step 1: Image → Caption
    caption_gen = CaptionGenerator(img_to_text_model)
    captions = caption_gen.process_batch([test_image])
    caption = captions[0]
    logger.info(f"\n1. CAPTION GENERATED:")
    logger.info(f"   {caption}")
    
    # Step 2: Caption → Normalized Text
    text_normalizer = TextNormalizer(text_norm_model)
    normalized_texts = text_normalizer.process_batch([caption])
    normalized = normalized_texts[0]
    logger.info(f"\n2. NORMALIZED TEXT:")
    logger.info(f"   {normalized}")
    
    # Step 3: Generate Embedding
    embedding_gen = EmbeddingGenerator(embedding_model)
    embeddings = embedding_gen.process_batch([normalized])
    embedding = embeddings[0]
    logger.info(f"\n3. EMBEDDING GENERATED:")
    logger.info(f"   Shape: {embedding.shape}")
    logger.info(f"   First 10 values: {embedding[:10]}")
    
    logger.info("\n")
    logger.info("ALL MODELS WORKING SUCCESSFULLY!")
    logger.info("\nNext step: Set up PostgreSQL to run full pipeline")

if __name__:
    main()
