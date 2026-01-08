# 🔍 Fashion Search Engine : 

An AI-powered fashion image search system that allows users to find fashion images using natural language text queries.The system understands clothing descriptions, colors, accessories, and context by combining Vision-Language Models, Text Normalization, Vector Search, and Re-Ranking.

This repository focuses on the Indexing Pipeline (Offline) and the Retrieval Pipeline (Online) used in real-world industry systems.
Traditional e-commerce search relies on fixed filters and manual tagging, which often fails to capture user intent.
This project demonstrates how VLM + NLP + vector databases can solve this problem in a scalable and intelligent way.

---

## 📋 Table of Contents : 

- [Key Features](#Key_Features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Configuration](#configuration)
- [Performance](#performance)

---

## ✨ Key Features : 

1. Natural language fashion search (no hard-coded filters)
2. Image → Text understanding using Vision-Language Models
3. Robust text normalization using LLMs
4. Fast semantic search using FAISS (vector database)
5. Accurate results using CLIP-based re-ranking
6. able metadata storage using PostgreSQL
7. Fully offline (all models run locally)

- **Multi-Model AI Pipeline**
  
  - Image captioning with    : Qwen2-VL-2B-Instruct
  - Text normalization with  : Qwen2.5-0.5B-Instruct
  - Semantic embeddings with : BAAI/bge-large-en-v1.5 (1024-dim)
  - Visual reranking with    :  CLIP ViT-L/14

- **Robust Storage**
  
  - PostgreSQL for metadata : ( image id , image path )  for fast Retrievel
  - FAISS for vector similarity search
  - Automatic deduplication

- **Modern Interface**
  
  - Interactive Streamlit web UI
  - Real-time search results 
  - Adjustable search parameters ( Top - K )
    
--- 

## 🧩 System Architecture Overview : 

| Stage              | What Happens               | Concept Used            |
| ------------------ | -------------------------- | ----------------------- |
| Image Captioning   | Converts image to text     | Vision-Language Model   |
| Text Normalization | Cleans & standardizes text | LLM Text Reasoning      |
| Embedding          | Converts text to vectors   | Semantic Embeddings     |
| Vector Storage     | Stores embeddings          | Vector Database (FAISS) |
| Retrieval          | Finds similar vectors      | Cosine Similarity       |
| Re-Ranking         | Refines top results        | Cross-Modal Similarity  |

---


### System Architecture : 

<img width="1761" height="2201" alt="intelligent_Search_Engine_Final_Arch drawio" src="https://github.com/user-attachments/assets/59f9d6a0-b057-4421-8c5c-6638cf207364" />

---

## 🏆 Why Better Than Vanilla CLIP? : 

1. First: What is a Vanilla CLIP System ?

  Vanilla CLIP approach in a simple way :
      a.Encode all images using CLIP Image Encoder
      b.Encode user query using CLIP Text Encoder
      c.Compare both embeddings
      d.Return top results
   Direct Cross-Modal Similarity

2. Our System

   1. Deep Image Understanding

      > Vanilla CLIP
            Image to embedding directly
            No explicit understanding of:
              1. Clothes
              2. Colors
              3. Accessories
              4. Context
      > Our System 
        > Image to  *Rich text caption*  then embedding
        > CLIP “looks” at the image but our system understands and explains the image


  2. LLM-Based Text Normalization
          
   > Normalizes both:
      1. Image captions
      2. User queries
  
  3. Two-Stage Retrieval
     > Stage 1: FAISS semantic search (Top 20)
     > Stage 2: CLIP re-ranking (Top K)

   Why this is better
     1. Fast search + precise ranking
     2. Candidate Generation + Re-Ranking

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


# SetUp : ( Offline +  Online )


## 🔧 Prerequisites

| Component            | Requirement                                           |
| -------------------- | ----------------------------------------------------- |
| Programming Language | Python 3.13+                                          |
| Database             | PostgreSQL 18                                         |
| GPU                  | NVIDIA GPU with CUDA (optional but recommended)       |
| Memory (RAM)         | 8 GB or higher                                        |
| Disk Space           | ~10 GB (for models and indexes)                       |

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

### Indexing Images ( Offiline )

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

### Running Search Interface  ( Online)

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

## FAISS Index
- Type: IndexFlatIP (Inner Product)
- Dimension: 1024
- Normalized vectors for cosine similarity

---

