# 🔍 Fashion Search Engine

The Intelligent Fashion Search Engine is an AI-powered fashion retrieval system that allows users to search fashion products using natural language text queries (e.g., "A person in a bright yellow raincoat") instead of traditional filters.

It combines computer vision, natural language processing, and vector similarity search to retrieve visually and semantically similar fashion items efficiently, even at large scale (up to 1 million images).

Traditional e-commerce search relies on fixed filters and manual tagging, which often fails to capture user intent.
This project demonstrates how VLM + NLP + vector databases can solve this problem in a scalable and intelligent way.

## 📋 Table of Contents

- [System Architecture](#system-architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Configuration](#configuration)
- [Performance](#performance)


### System Architecture

<img width="1761" height="2201" alt="intelligent_Search_Engine_Final_Arch drawio" src="https://github.com/user-attachments/assets/59f9d6a0-b057-4421-8c5c-6638cf207364" />


## ✨ Features

- **Multi-Model AI Pipeline**
  - Image captioning with Qwen2-VL-2B-Instruct
  - Text normalization with Qwen2.5-0.5B-Instruct
  - Semantic embeddings with BAAI/bge-large-en-v1.5 (1024-dim)
  - Visual reranking with CLIP ViT-L/14

- **Robust Storage**
  - PostgreSQL for metadata
  - FAISS for vector similarity search
  - Automatic deduplication

- **Modern Interface**
  - Interactive Streamlit web UI
  - Real-time search results
  - Adjustable search parameters

## 🔧 Prerequisites

| Component            | Requirement                                           |
| -------------------- | ----------------------------------------------------- |
| Programming Language | Python 3.13+                                          |
| Database             | PostgreSQL 18                                         |
| GPU                  | NVIDIA GPU with CUDA 13.0+ (optional but recommended) |
| Memory (RAM)         | 8 GB or higher                                        |
| Disk Space           | 10 GB or more (for models and indexes)                |

## Technology Stack

| Component            | Technology                  |
| -------------------- | --------------------------- |
| Programming Language | Python                      |
| Web Interface        | Streamlit                   |
| Image Captioning     | Vision-Language Model       |
| Embeddings           | CLIP-based Multimodal Model |
| Vector Database      | FAISS                       |
| Metadata Storage     | PostgreSQL                  |
| Hardware             | GPU-supported (local)       |


## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/PrashantTakale369/Intelligent_Fashion_Search_Engine.git
cd Intelligent_Fashion_Search_Engine
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

```bash
# Start PostgreSQL service
# Windows: services.msc → PostgreSQL
# Linux: sudo systemctl start postgresql

# Create database
psql -U postgres -c "CREATE DATABASE fashion_search;"
```

### 5. Initialize Database Schema

```bash
cd Indexing_Pipeline
python setup_database.py
```

## 🚀 Usage

### Indexing Images

Process fashion images to build the search index:

```bash
cd Indexing_Pipeline
python run_indexing.py
```

**Expected Output:**
```
✓ Loaded no of  images
✓ Generated captions
✓ Normalized text 
✓ Created embeddings
✓ Saved to PostgreSQL 
✓ Built FAISS index 
```

### Running Search Interface

Launch the Streamlit web application:

```bash
streamlit run app.py
```

Access the UI at **http://localhost:8501**

### Command-Line Testing

Test retrieval pipeline directly:

```bash
cd Retrieval_Pipeline
python run_test.py
```

## 📁 Project Full Architecture 

Fashion_Search_Engine/ │ ├── 📄 app.py # Streamlit Web UI (Main Entry Point) ├── 📄 requirements.txt # Python Dependencies ├── 📄 README.md # Main Documentation (This File) ├── 📄 download_model.txt # Model Download Instructions ├── 📄 how_to_run.txt # Quick Start Guide │ ├── 📁 Dataset/ # Fashion Images Storage │ └── 📁 Orignal_Dataset/ # Raw Fashion Images │ ├── 🖼️ image_001.jpg │ ├── 🖼️ image_002.png │ └── 🖼️ ... │ ├── 📁 Indexing_Pipeline/ # Image Processing & Database Creation │ │ │ ├── 📄 __init__.py # Package Initializer │ ├── 📄 README.md # Indexing Pipeline Documentation │ ├── 📄 run_indexing.py # Main Indexing Entry Point │ ├── 📄 test_models_only.py # Model Testing Without Database │ │ │ ├── 📁 config/ # Configuration Management │ │ └── 📄 indexing.yaml # Database, Models, Paths Settings │ │ │ ├── 📁 models/ # AI Model Wrappers │ │ ├── 📄 __init__.py │ │ ├── 📄 img_to_text_model.py # Qwen2-VL-2B (Image → Caption) │ │ ├── 📄 text_norm_model.py # Qwen2.5-0.5B (Caption → Features) │ │ └── 📄 embedding_model.py # BGE-large (Features → Vectors) │ │ │ ├── 📁 logic/ # Business Logic & Workflows │ │ ├── 📄 __init__.py │ │ ├── 📄 caption_logic.py # Caption Generation Pipeline │ │ ├── 📄 normalization_logic.py # Feature Extraction Pipeline │ │ └── 📄 embedding_logic.py # Vector Creation Pipeline │ │ │ ├── 📁 storage/ # Database Operations │ │ ├── 📄 __init__.py │ │ ├── 📄 schema.sql # PostgreSQL Database Schema │ │ ├── 📄 postgres_writer.py # PostgreSQL Write Operations │ │ ├── 📄 faiss_writer.py # FAISS Index Writer │ │ ├── 💾 faiss_index.bin # Generated: Vector Index File │ │ └── 💾 faiss_index_ids.npy # Generated: ID Mapping File │ │ │ ├── 📁 data/ # Dataset Management │ │ ├── 📄 __init__.py │ │ ├── 📄 dataset_loader.py # Image Loading & Validation │ │ └── 📄 image_registry.py # Image ID Tracking │ │ │ ├── 📁 utils/ # Helper Utilities │ │ ├── 📄 __init__.py │ │ ├── 📄 logger.py # Logging Configuration │ │ ├── 📄 batching.py # Batch Processing Utilities │ │ └── 📄 validation.py # Input Validation Functions │ │ │ └── 📁 scripts/ # Setup & Maintenance Scripts │ ├── 📄 README.md # Scripts Documentation │ ├── 📄 setup_database.py # Database Initialization │ └── 📄 clear_db.py # Database Cleanup Script │ ├── 📁 Retrieval_Pipeline/ # Search & Query Engine │ │ │ ├── 📄 __init__.py # Package Initializer │ ├── 📄 README.md # Retrieval Pipeline Documentation │ ├── 📄 retrieval_pipeline.py # Main Retrieval Orchestrator │ ├── 📄 run_test.py # Command-Line Search Testing │ │ │ ├── 📁 config/ # Configuration Management │ │ └── 📄 retrieval.yaml # Search Parameters, Model Settings │ │ │ ├── 📁 models/ # AI Model Wrappers │ │ ├── 📄 __init__.py │ │ └── 📄 clip_reranking_model.py # CLIP ViT-L/14 (Visual Reranking) │ │ │ ├── 📁 logic/ # Business Logic & Workflows │ │ ├── 📄 __init__.py │ │ ├── 📄 query_normalization.py # Query Text Normalization │ │ ├── 📄 query_embedding.py # Query Vector Generation │ │ └── 📄 reranking.py # CLIP-based Result Reranking │ │ │ ├── 📁 storage/ # Database Operations │ │ ├── 📄 __init__.py │ │ ├── 📄 faiss_searcher.py # FAISS Vector Search │ │ └── 📄 postgres_reader.py # PostgreSQL Read Operations │ │ │ └── 📁 utils/ # Helper Utilities │ ├── 📄 __init__.py │ └── 📄 logger.py # Logging Configuration │ └── 📁 ui/ # User Interface Components ├── 📄 __init__.py └── 📄 ui_components.py # Streamlit UI Widgets & Layouts

## ⚙️ Configuration

See individual pipeline READMEs for detailed architecture:
### Indexing Configuration 
[Indexing Pipeline README](Indexing_Pipeline/README.md)
### Retrieval Configuration
[Retrieval Pipeline README](Retrieval_Pipeline/README.md)


## 🔍 Search Quality

The system uses a two-stage retrieval approach:

1. **Semantic Search (FAISS)**
   - Fast initial retrieval
   - Text-based similarity
   - Returns top-20 candidates

2. **Visual Reranking (CLIP)**
   - Image-text alignment
   - More accurate final ranking
   - Returns top-10 results

This hybrid approach balances speed and accuracy.


## Scalability & Performance
  FAISS enables fast approximate nearest neighbor search
  Batch processing during indexing
  Separate storage for vectors and metadata
  GPU acceleration for heavy model inference

### Model Sizes

- Qwen2-VL-2B-Instruct: ~4.5GB
- Qwen2.5-0.5B-Instruct: ~1GB
- BAAI/bge-large-en-v1.5: ~1.3GB
- CLIP ViT-L/14: ~1.7GB
- **Total:** ~8.5GB

## FAISS Index
- Type: IndexFlatIP (Inner Product)
- Dimension: 1024
- Normalized vectors for cosine similarity


