# 🔍 Fashion Indexing Pipeline 

This pipeline processes your fashion images through models and creates a searchable database. If you're new to this project, follow this guide step by step.

---

## Pipeline Flow Architectre
<img width="1451" height="802" alt="Index_Pipline drawio" src="https://github.com/user-attachments/assets/32ff1dca-c773-427f-90a3-d10ab6e1ef8f" />

---

## 📖 Table of Contents

1. [What This Pipeline Does](#what-this-pipeline-does)
2. [What You Need Before Starting](#what-you-need-before-starting)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Preparing Your Dataset](#preparing-your-dataset)
5. [Running the Pipeline](#running-the-pipeline)
6. [Understanding the Files](#understanding-the-files)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## 🎯 What This Pipeline Does

The Indexing Pipeline transforms your fashion images into searchable data using AI:

```
Your Fashion Image - AI Processing - Searchable Database
```

**Example Flow:**
```
1. Input:  Image of a person wearing blue shirt
2. AI Caption:  "A person wearing a blue plaid shirt, black pants"
3. AI Normalize:  "shirt | blue | plaid | black pants |"
4. AI Embedding:  [0.003, -0.021, 0.145, ... ] (1024 numbers)
5. Storage:  Saved to database for fast searching
```
---

## Main Architectre

```
Indexing_Pipeline/
│
├── 📄 run_indexing.py                # Main execution script
├── 📄 test_models_only.py            # Model testing
│
├── 📁 config/
│   └── indexing.yaml                 # Pipeline configuration
│
├── 📁 data/
│   ├── dataset_loader.py             # Load images from Dataset/
│   └── image_registry.py             # Track processed images
│
├── 📁 models/
│   ├── img_to_text_model.py          # Qwen2-VL (Image - Caption)
│   ├── text_norm_model.py            # Qwen2.5 (Normalize text)
│   └── embedding_model.py            # BGE (Text - Vector)
│
├── 📁 logic/
│   ├── caption_logic.py              # Captioning orchestration
│   ├── normalization_logic.py        # Normalization orchestration
│   └── embedding_logic.py            # Embedding generation
│
├── 📁 storage/
│   ├── postgres_writer.py            # Save metadata to DB
│   ├── faiss_writer.py               # Save vectors to FAISS
│   └── schema.sql                    # Database schema
│
├── 📁 scripts/
│   ├── setup_database.py             # Initialize DB
│   └── clear_db.py                   # Clear all data
│
└── 📁 utils/
    ├── batching.py                   # Batch processing
    ├── logger.py                     # Logging
    └── validation.py                 # Input validation
```

---

## 📥 Step-by-Step Setup

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
git clone https: https://github.com/PrashantTakale369/Intelligent_Fashion_Search_Engine.git
cd Intelligent_Fashion_Search_Engine
```

### Step 2: Install Python Dependencies

Open terminal in the project root folder and run:

```bash
pip install -r requirements.txt
```

---

### Step 3: Download AI Models

The pipeline uses 3 AI models. Run these commands **one by one**:

```bash
# Model 1: Image Captioning (Qwen2-VL-2B-Instruct) - 
python -c "from transformers import Qwen2VLForConditionalGeneration, AutoProcessor; AutoProcessor.from_pretrained('Qwen/Qwen2-VL-2B-Instruct'); Qwen2VLForConditionalGeneration.from_pretrained('Qwen/Qwen2-VL-2B-Instruct')"

# Model 2: Text Normalization (Qwen2.5-0.5B-Instruct) - 
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct'); AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')"

# Model 3: Text Embeddings (BAAI/bge-large-en-v1.5) -
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('BAAI/bge-large-en-v1.5'); AutoModel.from_pretrained('BAAI/bge-large-en-v1.5')"
```

---

> **Note:** Models download once and are cached. Next time will be instant!

### Step 4: Setup PostgreSQL Database

**Method 1: Automatic Setup (Recommended)**

```bash
cd Indexing_Pipeline
python scripts/setup_database.py
```

This creates a database named `fashion_search` with the required table.

---

**Important:** Note your PostgreSQL password - you'll need it in the next step!

---

### Step 5: Configure the Pipeline

Edit the configuration file: `Indexing_Pipeline/config/indexing.yaml`

**Open the file and update these sections:**

---

```yaml
# Database Connection Settings
database:
  postgres:
    host: "localhost"          # Keep as is (local database)
    port: 5432                 # Keep as is (default PostgreSQL port)
    dbname: "fashion_search"   # Database name
    user: "postgres"           # Your PostgreSQL username
    password: "YOUR_PASSWORD"  # ⚠️ CHANGE THIS to your PostgreSQL password
  
  faiss:
    index_path: "storage/faiss_index.bin"  # Keep as is
    ids_path: "storage/faiss_index_ids.npy"  # Keep as is

# AI Model Settings
models:
  img_to_text:
    device: "cuda"  # Use "cuda" if you have NVIDIA GPU, "cpu" otherwise
    
  text_normalization:
    device: "cuda"  # Use "cuda" if you have NVIDIA GPU, "cpu" otherwise
    
  embedding:
    device: "cuda"  # Use "cuda" if you have NVIDIA GPU, "cpu" otherwise

# Dataset Settings
dataset:
  image_dir: "../Dataset/Orignal_Dataset"  # Path to your images
  batch_size: 4  # Process 4 images at once (reduce if GPU runs out of memory)
```
--- 

**GPU or CPU?**
- No GPU or errors? → Use `device: "cpu"` (works on any computer)

---

### Get Fashion Images

**Option 1 : Fashion Datasets**
https://drive.google.com/drive/folders/1AmMQMtgYGXIdS-tfDHuOyPdSVdrnTOFm?usp=sharing

---

## 📁 Preparing Your Dataset

### Where to Put Your Images

**Default Location:**
```
Fashion_Pipline_Engines/
└── Dataset/
    └── Orignal_Dataset/        ← Put your images here!
        ├── image_001.jpg
        ├── image_002.jpg
        ├── image_003.png
        └── ...
```

---

### How Many Images Do I Need?

- **Testing:** Start with 10-20 images
- **Small Project:** 1000-3000 images
- **Production:** 10000+ images

---

## ▶️ Running the Pipeline

### Quick Start (First Time)

Once everything is set up, run the indexing pipeline from the project root:

```bash
# Navigate to the project root
cd Intelligent_Fashion_Search_Engine

# Run the indexing pipeline
python Indexing_Pipeline/run_indexing.py
```

---

### What Happens When You Run It?

The pipeline will process each image through these steps:

```
Step 1: Load Images
  → Scanning Dataset/Orignal_Dataset/...
  → Found 4 images

Step 2: Generate Captions (AI Model 1)
  → Image 1: "A person wearing a blue plaid shirt..."
  → Image 2: "A person in a red jacket..."
  → Progress: [████████████████████] 4/4

Step 3: Normalize Text (AI Model 2)
  → Extracting features...
  → "shirt | blue | plaid | short sleeve | ..."
  → Progress: [████████████████████] 4/4

Step 4: Store in PostgreSQL
  → Inserting records into fashion_images table...
  → ✓ Saved 4 records

Step 5: Generate Embeddings (AI Model 3)
  → Creating 1024-dim vectors...
  → Progress: [████████████████████] 4/4

Step 6: Build FAISS Index
  → Adding vectors to index...
  → ✓ Saved faiss_index.bin
  → ✓ Saved faiss_index_ids.npy

 INDEXING COMPLETE!
   Processed: 4 images
   Time: 38 seconds (GPU) or 4.5 minutes (CPU)
```
---

### Output Files

After running successfully, you'll find:

```
Indexing_Pipeline/
└── storage/
    ├── faiss_index.bin         ← Vector index for fast search
    └── faiss_index_ids.npy     ← Mapping of vectors to image IDs
```

Plus records in your PostgreSQL database (`fashion_images` table).

---

## 🧪 Testing Before Full Run

---

### Test 1: Check Models Only (No Database)

Want to verify models work without setting up the database?

```bash
cd Fashion_Pipline_Engines
python Indexing_Pipeline/test_models_only.py
```

**What this does:**
- Loads all 3 AI models
- Processes one test image
- Shows caption, normalized text, and embedding
- **No database required!**

Expected output:
```
Loading models...
✓ Image-to-Text Model loaded
✓ Text Normalization Model loaded
✓ Embedding Model loaded

Processing image: Dataset/Orignal_Dataset/image_001.jpg
Caption: "A person wearing a blue plaid shirt, black pants..."
Normalized: "shirt | blue | plaid | short sleeve | black pants | ..."
Embedding shape: (1024,)

All models working correctly!
```
---

### Test 2: Database Connection

```bash
cd Indexing_Pipeline
python scripts/setup_database.py
```

If successful, you'll see:
```
✓ Connected to PostgreSQL
✓ Database 'fashion_search' exists
✓ Table 'fashion_images' created
```

### Test 3: Process Small Batch

Edit `config/indexing.yaml` and set:
```yaml
dataset:
  image_dir: "../Dataset/Orignal_Dataset"
  batch_size: 2  # Process only 2 images for testing
```

Then run the pipeline normally.

---

## 📂 Understanding the Files

---

### Core Files You'll Use

| File | What It Does | When to Use |
|------|--------------|-------------|
| `run_indexing.py` | Main entry point - runs the full pipeline | Every time you want to index images |
| `config/indexing.yaml` | All settings (database, models, paths) | When setting up or changing configuration |
| `scripts/setup_database.py` | Creates PostgreSQL database and tables | Once during initial setup |
| `test_models_only.py` | Tests AI models without database | When troubleshooting models 

---

## � Troubleshooting Common Issues

--- 

### Issue 1: "CUDA out of memory"

**Error:**
```
RuntimeError: CUDA out of memory. Tried to allocate X MiB
```

**Solution:**

1. **Reduce batch size** in `config/indexing.yaml`:
   ```yaml
   dataset:
     batch_size: 1  # Try 1 or 2 instead of 4
   ```

2. **Switch to CPU mode** (slower but works):
   ```yaml
   models:
     img_to_text:
       device: "cpu"
     text_normalization:
       device: "cpu"
     embedding:
       device: "cpu"
   ```
---

## 🔄 What's Next?

After indexing is complete, you can:

### 1. Use the Retrieval Pipeline

Search your indexed images:
```bash
cd Retrieval_Pipeline
python retrieval_pipeline.py
```

See `Retrieval_Pipeline/README.md` for details.

### 2. Launch the Web UI

```bash
streamlit run app.py
```

Opens a web interface at http://localhost:8501

---

### Model Information

- **Qwen2-VL:** https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct
- **Qwen2.5:** https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- **BGE Embeddings:** https://huggingface.co/BAAI/bge-large-en-v1.5
  
---

## 🎓 Understanding the AI Models

### Model 1: Qwen2-VL-2B-Instruct (Image Captioning)

**What it does:** Looks at image and describes what it sees  
**Input:** Image file  
**Output:** Text description  
**Example:**
```
Input: [Image of person in blue shirt]
Output: "A person wearing a blue plaid button-up shirt with short sleeves, black pants, and black sneakers."
```

### Model 2: Qwen2.5-0.5B-Instruct (Text Normalization)

**What it does:** Extracts key features from description  
**Input:** Natural language description  
**Output:** Structured features  
**Example:**
```
Input: "A person wearing a blue plaid button-up shirt..."
Output: "shirt | blue | plaid | button-up | short sleeve | black pants | sneakers |"
```

### Model 3: BAAI/bge-large-en-v1.5 (Embeddings)

**What it does:** Converts text to numbers for searching  
**Input:** Normalized text  
**Output:** 1024 numbers representing meaning  
**Example:**
```
Input: "shirt | blue | plaid | ..."
Output: [0.003, -0.021, 0.145, ..., 0.089]  (1024 numbers)
```
---
