# 🔍 Fashion Search Engine

The Intelligent Fashion Search Engine is an AI-powered fashion retrieval system that allows users to search fashion products using natural language text queries (e.g., "A person in a bright yellow raincoat") instead of traditional filters.

It combines computer vision, natural language processing, and vector similarity search to retrieve visually and semantically similar fashion items efficiently, even at large scale (up to 1 million images).

Traditional e-commerce search relies on fixed filters and manual tagging, which often fails to capture user intent.
This project demonstrates how VLM + NLP + vector databases can solve this problem in a scalable and intelligent way.

---

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Configuration](#configuration)
- [Performance](#performance)

---

### System Architecture

<img width="1761" height="2201" alt="intelligent_Search_Engine_Final_Arch drawio" src="https://github.com/user-attachments/assets/59f9d6a0-b057-4421-8c5c-6638cf207364" />

---

## 🏆 Why Better Than Vanilla CLIP?

This project uses a **hybrid, production-ready architecture** that separates semantic retrieval from visual re-ranking:

<table>
<tr>
<td width="30%"><strong>🔹 Specialized Semantic Embeddings</strong></td>
<td>
<ul>
<li><strong>BGE-Large (1024-dim)</strong> vs CLIP's 512-dim vectors (2× richer)</li>
<li>Trained specifically for <strong>text similarity</strong>, not vision-language alignment</li>
<li>Better semantic matching for fashion descriptions and user intent</li>
</ul>
</td>
</tr>

<tr>
<td width="30%"><strong>🔹 Advanced Pre-processing Pipeline</strong></td>
<td>
<ul>
<li><strong>Qwen2-VL</strong> generates detailed, human-like image captions</li>
<li><strong>Qwen2.5</strong> normalizes captions and user queries</li>
<li>Produces clean, searchable text instead of raw image embeddings</li>
</ul>
</td>
</tr>

<tr>
<td width="30%"><strong>🔹 Scalable Vector Search</strong></td>
<td>
<ul>
<li><strong>FAISS indexing</strong> enables sub-second similarity search</li>
<li>Replaces CLIP's O(n) brute-force comparison with efficient indexing</li>
<li>Supports millions of items without performance degradation</li>
</ul>
</td>
</tr>

<tr>
<td width="30%"><strong>🔹 CLIP as Re-ranker Only</strong></td>
<td>
<ul>
<li>BGE-based semantic search retrieves <strong>top-N candidates</strong></li>
<li>CLIP <strong>visually re-ranks</strong> only these N results</li>
<li>Combines semantic understanding with visual accuracy</li>
</ul>
</td>
</tr>

<tr>
<td width="30%"><strong>🔹 Persistent Storage</strong></td>
<td>
<ul>
<li><strong>PostgreSQL</strong> stores metadata permanently</li>
<li><strong>FAISS</strong> stores embeddings permanently</li>
<li>Eliminates re-encoding images on every search request</li>
</ul>
</td>
</tr>
</table>

**Result**: BGE's superior semantic understanding for initial retrieval + CLIP's visual intelligence for final ranking = faster, more accurate fashion search than vanilla CLIP alone.

---


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

--- 


## 🔧 Prerequisites

| Component            | Requirement                                           |
| -------------------- | ----------------------------------------------------- |
| Programming Language | Python 3.13+                                          |
| Database             | PostgreSQL 18                                         |
| GPU                  | NVIDIA GPU with CUDA 13.0+ (optional but recommended) |
| Memory (RAM)         | 8 GB or higher                                        |
| Disk Space           | 10 GB or more (for models and indexes)                |

---

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

---

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
# Create database
psql -U postgres -c "CREATE DATABASE fashion_search;"
```

### 5. Initialize Database Schema

```bash
cd Indexing_Pipeline
python setup_database.py
```

---

## 🚀 Start Processing 

---

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

--- 

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

--- 

## How This Work 


### **Step 1: Indexing (One-time Setup)**
1. Load fashion images from `Dataset/`
2. AI describes each image → "red dress with floral pattern"
3. Clean the description → "elegant red dress floral pattern women"
4. Convert text to numbers (vector) → [0.23, 0.45, ..., 0.89]
5. Save to database / vector index (FAISS)

### **Step 2: Search (Every Query)**
1. User types: "blue summer dress"
2. Clean query → "blue summer dress women"
3. Convert to vector → [0.12, 0.78, ..., 0.34]
4. FAISS finds 50 similar vectors → get matching images
5. CLIP AI visually reranks → best 10 results
6. Display images

---

## 📁 Main Architecture 

```
Intelligent_Fashion_Search_Engine/
│
├── 📄 app.py                          # Main Streamlit Application
├── 📄 requirements.txt                # Dependencies
├── 📄 README.md                       # Documentation
│
├── 📁 Dataset/                        # Fashion Images
├── 📁 Indexing_Pipeline/             # Image Processing Pipeline
├── 📁 Retrieval_Pipeline/            # Search & Retrieval Pipeline
└── 📁 ui/                            # User Interface Components
```

---

## ⚙️ Configuration

See individual pipeline READMEs for detailed architecture:
### Indexing Configuration 
[Indexing Pipeline README](Indexing_Pipeline/README.md)
### Retrieval Configuration
[Retrieval Pipeline README](Retrieval_Pipeline/README.md)

---

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

---

## ⚙️ Scalability & Performance

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

---

