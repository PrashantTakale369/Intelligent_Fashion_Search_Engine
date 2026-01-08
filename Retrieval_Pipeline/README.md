r# 🔍 Fashion Retrieval Pipeline - Search Your Images

This pipeline lets you search through your fashion images using everyday language like "red dress" or "blue jacket". If you're new to this project, follow this guide step by step.

---

## Main Architectre
<img width="1517" height="1212" alt="Retrieval_Pipeline drawio" src="https://github.com/user-attachments/assets/9d821c06-64c9-403e-a15f-eb598a9074eb" />


## 📖 Table of Contents

1. [What This Pipeline Does](#what-this-pipeline-does)
2. [Before You Start](#before-you-start)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Running Your First Search](#running-your-first-search)
5. [Using the Web Interface](#using-the-web-interface)
6. [Understanding the Files](#understanding-the-files)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## 🎯 What This Pipeline Does

The Retrieval Pipeline searches your indexed fashion images using AI:

```
Your Text Query → AI Processing → Search Results with Images
```

**Example:**
```
1. You type:     "A person in a bright yellow raincoat."
3. AI searches:  Finds similar images in database
4. AI reranks:   Uses visual matching for best results
5. You get:      Top 10 most relevant images!
```

**Why This Matters:** Instead of manually browsing thousands of images, just describe what you're looking for and get instant results!

---

## Before You Start

### Requirements Checklist

**You MUST have completed these first:**

1. **Indexing Pipeline Done** 
   - You should have already run the Indexing Pipeline
   - Check: Do you have these files?
     - `Indexing_Pipeline/storage/faiss_index.bin`
     - `Indexing_Pipeline/storage/faiss_index_ids.npy`
   - If NO → Go back and run the Indexing Pipeline first!

2. **PostgreSQL Database Populated** 
   - Your fashion_images table should have data
   - Check by running:
     ```sql
     SELECT COUNT(*) FROM fashion_images;
     ```
   - Should return a number > 0

3. **Dataset Still Available** 
   - Your original images must still be in the same location
   - Default: `Dataset/Orignal_Dataset/`

**If any of the above are missing, the search won't work!**

### Software Requirements

Same as Indexing Pipeline:
- Python 3.8+
- PostgreSQL (already running)
- NVIDIA GPU (optional, for speed)
  
---

## 📥 Step-by-Step Setup

### Step 1: Verify Prerequisites

Make sure you've completed the Indexing Pipeline:

```powershell
# Check if FAISS index exists
Get-ChildItem -Path "Indexing_Pipeline\storage" -Filter "faiss*"

# Should show:
# faiss_index.bin
# faiss_index_ids.npy
```

### Step 2: Install Additional Dependencies (if needed)

Most dependencies are already installed from Indexing Pipeline, but check:

```bash
pip install streamlit pillow
```

### Step 3: Download CLIP Model

The Retrieval Pipeline uses one additional model for reranking:

```bash
# CLIP Model for visual reranking (~1.7 GB)
python -c "from transformers import CLIPProcessor, CLIPModel; CLIPProcessor.from_pretrained('openai/clip-vit-large-patch14'); CLIPModel.from_pretrained('openai/clip-vit-large-patch14')"
```

⏳ This downloads once and is cached.

### Step 4: Configure Settings

Edit `Retrieval_Pipeline/config/retrieval.yaml`:

```yaml
# Database Connection (same as Indexing Pipeline)
database:
  postgres:
    host: "localhost"
    port: 5432
    dbname: "fashion_search"
    user: "postgres"
    password: "YOUR_PASSWORD"  # ⚠️ Same as indexing config
  
  faiss:
    # Path to FAISS index created by Indexing Pipeline
    index_path: "../Indexing_Pipeline/storage/faiss_index.bin"
    ids_path: "../Indexing_Pipeline/storage/faiss_index_ids.npy"

# Dataset (where your images are)
dataset:
  image_dir: "../Dataset/Orignal_Dataset"

# AI Models
models:
  text_normalization:
    device: "cuda"  # "cuda" for GPU, "cpu" for CPU
  
  embedding:
    device: "cuda"  # "cuda" for GPU, "cpu" for CPU
  
  reranking:
    device: "cuda"  # "cuda" for GPU, "cpu" for CPU

# Search Settings
search:
  top_n: 20  # How many candidates to get from semantic search
  top_k: 10  # Final number of results to show
```

**Important:** Make sure `faiss.index_path` points to your actual FAISS index!

---

## 🚀 Running Your First Search

### Method 1: Quick Test (Command Line)

Run a test search to verify everything works:

```bash
cd Fashion_Pipline_Engines/Retrieval_Pipeline
python run_test.py
```

**What happens:**
```
Loading models...
Text Normalization Model loaded
Embedding Model loaded
CLIP Reranking Model loaded
FAISS Index loaded (4 vectors)
Database connected

Running test query: "A person in a bright yellow raincoat"

Step 1: Normalizing query...
  → "person | raincoat | yellow | bright"

Step 2: Creating embedding...
  → Vector shape: (1024,)

Step 3: Searching FAISS index...
  → Found 4 candidates

Step 4: Reranking with CLIP...
  → Reranked to top 4 results

Results:
1. Image ID: 7 | Semantic Score: 0.5146 | CLIP Score: 0.1455
   Path: Dataset/Orignal_Dataset/7.jpg
   
2. Image ID: 1 | Semantic Score: 0.4990 | CLIP Score: 0.1438
   Path: Dataset/Orignal_Dataset/1.jpg
...

```

**If you see results like above - Everything works!**

---

## 🌐 Using the Web Interface

### Launch the Streamlit App

```bash
cd Fashion_Pipline_Engines
streamlit run app.py
```

**You'll see:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.X:8501
```

Open **http://localhost:8501** in your browser!

---

### Using the Web UI

**Search Interface:**

1. **Enter Your Query**
   - Type what you're looking for: "A person in a bright yellow raincoat.""
   - Natural language works: "person wearing yellow jacket"

2. **Click Search Button**
   - Results appear in ~1-2 seconds
   - Shows images in a grid

3. **View Results**
   - Clean image grid
   - Click images to view larger
   - Images displayed in relevance order

### Sidebar Settings (Optional)

You can adjust search parameters in the sidebar:

- **Final Results (Top-K):** 1-20
  - How many images to show in final results
  - Default: 10

---

## 🔍 How Search Works (Behind the Scenes)

### Why Two Stages?

**Stage 1 (FAISS Semantic Search):**
- **Super fast** - searches millions of images in milliseconds
- **Text-based** - compares text descriptions
- **Broad net** - gets many candidates

**Stage 2 (CLIP Reranking):**
- **More accurate** - actually looks at the images
- **Visual matching** - text-to-image comparison
- **Slower** - processes actual image pixels
- **Refinement** - picks best from candidates

**Together:** Fast + accurate! 🚀

---

## 📂 Understanding the Files

### Files You'll Use

| File | Purpose | When to Use |
|------|---------|-------------|
| `retrieval_pipeline.py` | Main search engine | When integrating into your code |
| `run_test.py` | Quick test script | To verify search works |
| `config/retrieval.yaml` | All settings | When changing configuration |
| `../app.py` | Web interface | For user-friendly searching |

### Pipeline Internals (Auto-loaded)

```
Retrieval_Pipeline/
│
├── models/                     # AI model wrappers
│   └── clip_reranking_model.py    # CLIP for visual reranking
│
├── logic/                      # Search workflows
│   ├── query_normalization.py     # Normalize user query
│   ├── query_embedding.py         # Convert to vector
│   └── reranking.py               # CLIP reranking
│
├── storage/                    # Data access
│   ├── faiss_searcher.py          # Search FAISS index
│   └── postgres_reader.py         # Fetch from database
│
└── utils/                      # Helpers
    └── logger.py                   # Logging
```

**You don't need to edit these unless customizing the pipeline.**

---

## 🔧 Troubleshooting

### Issue 1: "FAISS index not found"

**Error:**
```
FileNotFoundError: faiss_index.bin not found
```

**Solutions:**

1. **Run Indexing Pipeline first!**
   ```bash
   cd Indexing_Pipeline
   python run_indexing.py
   ```

2. **Check path in config:**
   ```yaml
   database:
     faiss:
       index_path: "../Indexing_Pipeline/storage/faiss_index.bin"
   ```

3. **Verify files exist:**
   ```powershell
   Get-ChildItem "Indexing_Pipeline\storage\faiss*"
   ```

---

### Issue 2: "Database connection failed"

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**

1. **Check PostgreSQL is running:**
   ```powershell
   Get-Service postgresql*
   ```

2. **Verify credentials** in `config/retrieval.yaml`:
   ```yaml
   database:
     postgres:
       password: "your_password"  # Check this!
   ```

3. **Test database has data:**
   ```sql
   SELECT COUNT(*) FROM fashion_images;
   ```

---

## 📚 Additional Resources

### Models Used

| Model | Purpose | Documentation |
|-------|---------|---------------|
| Qwen2.5-0.5B-Instruct | Query normalization | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct |
| BAAI/bge-large-en-v1.5 | Text embeddings | https://huggingface.co/BAAI/bge-large-en-v1.5 |
| CLIP ViT-L/14 | Visual reranking | https://huggingface.co/openai/clip-vit-large-patch14 |

---

## 🎓 Understanding the Technology

### What is CLIP?

**CLIP** (Contrastive Language-Image Pre-training) understands both images and text.

**How it works:**
1. Trained on 400 million image-text pairs
2. Learned to match images with their descriptions
3. Can compare any text to any image
4. Gives a score for how well they match

**Why we use it:**
- More accurate than text-only matching
- Actually "looks" at the image
- 
### Why Two-Stage Search?

**Stage 1 (FAISS):** Fast rough filter
- Searches 100,000 images in 0.01 seconds
- Text-based similarity
- Gets top 20 candidates

**Stage 2 (CLIP):** Accurate refinement
- Looks at actual images
- Visual-semantic matching
- Reranks top 20 → final top 10
