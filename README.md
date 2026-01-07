# 🔍 Fashion Search Engine

A complete AI-powered fashion image search engine with semantic search and CLIP-based reranking, featuring GPU acceleration and a modern Streamlit interface.

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Configuration](#configuration)
- [Performance](#performance)

## 🎯 Overview

This project implements a two-stage AI pipeline for fashion image search:

1. **Indexing Pipeline**: Processes fashion images through multiple AI models to generate searchable embeddings
2. **Retrieval Pipeline**: Performs semantic search with CLIP reranking for accurate fashion item discovery

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INDEXING PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Image → Captioning → Normalization → Embedding → Storage  │
│         (Qwen2-VL)   (Qwen2.5)       (BGE)     (PG+FAISS)  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   RETRIEVAL PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Query → Normalize → Embed → Semantic Search → CLIP Rerank │
│         (Qwen2.5)   (BGE)    (FAISS Top-20)   (Top-10)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    Streamlit Web UI
```

## ✨ Features

- **Multi-Model AI Pipeline**
  - Image captioning with Qwen2-VL-2B-Instruct
  - Text normalization with Qwen2.5-0.5B-Instruct
  - Semantic embeddings with BAAI/bge-large-en-v1.5 (1024-dim)
  - Visual reranking with CLIP ViT-L/14

- **High Performance**
  - GPU acceleration (CUDA support)
  - Batch processing for efficiency
  - 7x faster with GPU vs CPU
  - Processes 7 images in ~38 seconds

- **Robust Storage**
  - PostgreSQL for metadata
  - FAISS for vector similarity search
  - Automatic deduplication

- **Modern Interface**
  - Interactive Streamlit web UI
  - Real-time search results
  - Adjustable search parameters
  - Visual result display with scores

## 🔧 Prerequisites

- Python 3.13+
- PostgreSQL 18
- NVIDIA GPU with CUDA 13.0+ (optional but recommended)
- 8GB+ RAM
- 10GB+ disk space for models

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/PrashantTakale369/fashion.git
cd Fashion_Pipline_Engines
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
✓ Loaded 7 images
✓ Generated captions (Qwen2-VL)
✓ Normalized text (Qwen2.5)
✓ Created embeddings (BGE)
✓ Saved to PostgreSQL (21 records)
✓ Built FAISS index (21 vectors)
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

## 📁 Pipeline Details

### Indexing Pipeline

**Location:** `Indexing_Pipeline/`

**Components:**
- `models/` - AI model wrappers (Qwen2-VL, Qwen2.5, BGE)
- `logic/` - Processing logic (captioning, normalization, embedding)
- `storage/` - Database writers (PostgreSQL, FAISS)
- `data/` - Dataset loading and validation
- `utils/` - Logging and batching utilities

**Process Flow:**
1. Load images from `Dataset/`
2. Generate 3 captions per image using Qwen2-VL
3. Normalize each caption to extract key features
4. Create 1024-dim embeddings with BGE
5. Store metadata in PostgreSQL
6. Build FAISS index for vector search

**Configuration:** `Indexing_Pipeline/config/indexing.yaml`

### Retrieval Pipeline

**Location:** `Retrieval_Pipeline/`

**Components:**
- `models/` - CLIP reranking model
- `logic/` - Query processing and reranking
- `storage/` - FAISS search and PostgreSQL reader
- `app.py` - Streamlit web interface
- `retrieval_pipeline.py` - Main orchestrator

**Process Flow:**
1. Normalize user query
2. Generate query embedding
3. FAISS semantic search (top-20)
4. CLIP reranking (top-10)
5. Return ranked results with scores

**Configuration:** `Retrieval_Pipeline/config/retrieval.yaml`

## ⚙️ Configuration

### Indexing Configuration

Edit `Indexing_Pipeline/config/indexing.yaml`:

```yaml
models:
  image_to_text:
    device: "cuda"  # or "cpu"
    batch_size: 4
  
  text_normalization:
    device: "cuda"
  
  embedding:
    device: "cuda"
    batch_size: 8

database:
  postgres:
    host: "localhost"
    password: "your_password"
```

### Retrieval Configuration

Edit `Retrieval_Pipeline/config/retrieval.yaml`:

```yaml
search:
  top_n: 20  # Semantic search results
  top_k: 10  # Final results after reranking

models:
  reranking:
    device: "cuda"
```

## 📊 Performance

### Hardware Specs (Test System)
- GPU: NVIDIA RTX 4060 (8GB VRAM)
- CPU: 24 threads
- RAM: 16GB
- CUDA: 13.0

### Benchmark Results

| Operation | GPU Time | CPU Time | Speedup |
|-----------|----------|----------|---------|
| Image Captioning (7 images) | ~25s | ~150s | 6x |
| Text Normalization (21 captions) | ~8s | ~45s | 5.6x |
| Embedding Generation (21 texts) | ~5s | ~40s | 8x |
| **Total Indexing** | **~38s** | **~235s** | **~7x** |
| FAISS Search | <0.1s | <0.1s | - |
| CLIP Reranking (20 images) | ~1s | ~8s | 8x |

### Model Sizes
- Qwen2-VL-2B-Instruct: ~4.5GB
- Qwen2.5-0.5B-Instruct: ~1GB
- BAAI/bge-large-en-v1.5: ~1.3GB
- CLIP ViT-L/14: ~1.7GB
- **Total:** ~8.5GB

## 🗃️ Database Schema

### PostgreSQL Table: `fashion_images`

```sql
CREATE TABLE fashion_images (
    image_id SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL UNIQUE,
    normalized_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### FAISS Index
- Type: IndexFlatIP (Inner Product)
- Dimension: 1024
- Normalized vectors for cosine similarity

## 🎨 Example Queries

- "A person in a bright yellow raincoat"
- "Blue denim jacket"
- "Red dress with black heels"
- "White sneakers"
- "Black leather bag"

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

## 📝 Quick Start

```bash
# 1. Index your images
cd Indexing_Pipeline
python run_indexing.py

# 2. Launch search interface
cd ../Retrieval_Pipeline
streamlit run app.py

# 3. Search for fashion items!
# Open http://localhost:8501 in your browser
```

## 🤝 Contributing

Contributions are welcome! See individual pipeline READMEs for detailed architecture:
- [Indexing Pipeline README](Indexing_Pipeline/README.md)
- [Retrieval Pipeline README](Retrieval_Pipeline/README.md)

## 📄 License

This project uses models with various licenses. Please check individual model licenses:
- Qwen models: Apache 2.0
- BGE: MIT
- CLIP: MIT

## 🔗 Links

- Repository: https://github.com/PrashantTakale369/fashion
- Models: HuggingFace Model Hub
