# 🔍 Fashion Indexing Pipeline

> **A beginner-friendly guide to setting up the AI-powered fashion image indexing system**

This pipeline processes your fashion images through AI models and creates a searchable database. If you're new to this project, follow this guide step by step.

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
Your Fashion Image → AI Processing → Searchable Database
```

**Example Flow:**
```
1. Input:  Image of a person wearing blue shirt
2. AI Caption:  "A person wearing a blue plaid shirt, black pants"
3. AI Normalize:  "shirt | blue | plaid | black pants |"
4. AI Embedding:  [0.003, -0.021, 0.145, ... ] (1024 numbers)
5. Storage:  Saved to database for fast searching
```

**Why This Matters:** After indexing, you can search your images using natural language like "red dress" or "blue jacket" and get relevant results instantly.

---

## 💻 What You Need Before Starting

### Required Software

1. **Python 3.8 or Higher**
   - Check: Open terminal/command prompt and run `python --version`
   - Download: https://www.python.org/downloads/

2. **PostgreSQL Database**
   - Why: Stores image information and descriptions
   - Download: https://www.postgresql.org/download/
   - During installation, remember your password!

3. **Git** (if cloning from GitHub)
   - Download: https://git-scm.com/downloads

### Recommended (Optional)

4. **NVIDIA GPU with CUDA**
   - Why: Makes processing **7x faster**
   - Check: Open terminal and run `nvidia-smi`
   - If you see GPU info, you're good to go!
   - Don't have GPU? No problem - CPU mode works fine (just slower)

### Storage Requirements

- **Disk Space:** At least 10-15 GB free
  - AI Models: ~8 GB
  - Your Dataset: Varies
  - Database: ~100 MB per 1000 images

- **RAM:** 8 GB minimum, 16 GB recommended

---

## 📥 Step-by-Step Setup

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
git clone https://github.com/PrashantTakale369/fashion.git
cd fashion
```

**Option B: Already Downloaded?**
```bash
cd path/to/Fashion_Pipline_Engines
```

### Step 2: Install Python Dependencies

Open terminal in the project root folder and run:

```bash
pip install -r requirements.txt
```

**What this installs:**
- PyTorch (AI framework)
- Transformers (for AI models)
- PostgreSQL connector
- FAISS (for fast search)
- And more...

⏳ This may take 5-10 minutes depending on your internet speed.

### Step 3: Download AI Models

The pipeline uses 3 AI models. Run these commands **one by one**:

```bash
# Model 1: Image Captioning (Qwen2-VL-2B-Instruct) - ~4 GB
python -c "from transformers import Qwen2VLForConditionalGeneration, AutoProcessor; AutoProcessor.from_pretrained('Qwen/Qwen2-VL-2B-Instruct'); Qwen2VLForConditionalGeneration.from_pretrained('Qwen/Qwen2-VL-2B-Instruct')"

# Model 2: Text Normalization (Qwen2.5-0.5B-Instruct) - ~1 GB
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct'); AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')"

# Model 3: Text Embeddings (BAAI/bge-large-en-v1.5) - ~1.3 GB
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('BAAI/bge-large-en-v1.5'); AutoModel.from_pretrained('BAAI/bge-large-en-v1.5')"
```

⏳ **Total download:** ~8 GB, may take 10-30 minutes on first run.

💡 **Note:** Models download once and are cached. Next time will be instant!

### Step 4: Setup PostgreSQL Database

**Method 1: Automatic Setup (Recommended)**

```bash
cd Indexing_Pipeline
python scripts/setup_database.py
```

This creates a database named `fashion_search` with the required table.

**Method 2: Manual Setup**

1. Open PostgreSQL (pgAdmin or psql command line)
2. Create a new database:
   ```sql
   CREATE DATABASE fashion_search;
   ```
3. Run the schema file:
   ```bash
   psql -U postgres -d fashion_search -f Indexing_Pipeline/storage/schema.sql
   ```

**Important:** Note your PostgreSQL password - you'll need it in the next step!

### Step 5: Configure the Pipeline

Edit the configuration file: `Indexing_Pipeline/config/indexing.yaml`

**Open the file and update these sections:**

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

**GPU or CPU?**
- Have NVIDIA GPU? → Use `device: "cuda"` (7x faster!)
- No GPU or errors? → Use `device: "cpu"` (works on any computer)

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

### Supported Image Formats

- ✅ `.jpg` / `.jpeg`
- ✅ `.png`
- ❌ `.gif`, `.bmp`, `.webp` (not supported yet)

### How to Get Fashion Images

Since we don't include the dataset in this repository, here are your options:

**Option 1: Use Your Own Images**
- Take photos of clothing items
- Download from online stores (check copyright!)
- Use your personal fashion photos

**Option 2: Public Fashion Datasets**
- **DeepFashion Dataset**: http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
- **Fashion-MNIST** (simple): https://github.com/zalandoresearch/fashion-mnist
- **Fashionpedia**: https://fashionpedia.github.io/home/index.html

**Option 3: Web Scraping**
- Use tools like `scrapy` or `selenium` to collect images
- **⚠️ Important:** Always respect copyright and terms of service

### Dataset Structure Tips

1. **Organize by folder (optional but helpful):**
   ```
   Dataset/Orignal_Dataset/
   ├── shirts/
   ├── pants/
   ├── dresses/
   └── shoes/
   ```

2. **Name files clearly:**
   - ✅ Good: `blue_shirt_001.jpg`, `red_dress_045.png`
   - ❌ Avoid: `IMG_1234.jpg`, `untitled.png`

3. **Image Quality:**
   - Resolution: At least 512x512 pixels recommended
   - Clear lighting and focus
   - Single clothing item per image works best

### How Many Images Do I Need?

- **Testing:** Start with 10-20 images
- **Small Project:** 100-500 images
- **Production:** 1,000+ images

---

## ▶️ Running the Pipeline

### Quick Start (First Time)

Once everything is set up, run the indexing pipeline from the project root:

```bash
# Navigate to the project root
cd Fashion_Pipline_Engines

# Run the indexing pipeline
python Indexing_Pipeline/run_indexing.py
```

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

✅ INDEXING COMPLETE!
   Processed: 4 images
   Time: 38 seconds (GPU) or 4.5 minutes (CPU)
```

### Processing Time Estimates

| Images | CPU Mode | GPU Mode (RTX 4060) |
|--------|----------|---------------------|
| 10     | ~6 min   | ~50 sec            |
| 50     | ~30 min  | ~4 min             |
| 100    | ~1 hour  | ~8 min             |
| 500    | ~5 hours | ~40 min            |

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

✅ All models working correctly!
```

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

### Core Files You'll Use

| File | What It Does | When to Use |
|------|--------------|-------------|
| `run_indexing.py` | Main entry point - runs the full pipeline | Every time you want to index images |
| `config/indexing.yaml` | All settings (database, models, paths) | When setting up or changing configuration |
| `scripts/setup_database.py` | Creates PostgreSQL database and tables | Once during initial setup |
| `test_models_only.py` | Tests AI models without database | When troubleshooting models |

### Pipeline Internals (You Don't Need to Edit These)

```
Indexing_Pipeline/
│
├── models/                    # AI model wrappers
│   ├── img_to_text_model.py      # Image captioning
│   ├── text_norm_model.py        # Text normalization
│   └── embedding_model.py        # Vector embeddings
│
├── logic/                     # Processing workflows
│   ├── caption_logic.py          # Caption generation
│   ├── normalization_logic.py    # Feature extraction
│   └── embedding_logic.py        # Embedding creation
│
├── storage/                   # Database operations
│   ├── postgres_writer.py        # Save to PostgreSQL
│   ├── faiss_writer.py           # Save to FAISS index
│   └── schema.sql                # Database structure
│
├── data/                      # Data loading
│   ├── dataset_loader.py         # Load images from disk
│   └── image_registry.py         # Track image IDs
│
└── utils/                     # Helper functions
    ├── logger.py                 # Logging messages
    ├── batching.py               # Batch processing
    └── validation.py             # Input validation
```

### How the Pipeline Works (Technical)

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR IMAGES                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  1. DatasetLoader     │
         │  • Finds all .jpg/.png│
         │  • Validates files    │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  2. ImageToTextModel  │
         │  (Qwen2-VL-2B)        │
         │  Image → Caption      │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  3. TextNormalizer    │
         │  (Qwen2.5-0.5B)       │
         │  Caption → Features   │
         └───────────┬───────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│ 4a. PostgreSQL  │    │ 4b. Embedding    │
│ • image_path    │    │ (BAAI BGE)       │
│ • norm_text     │    │ Text → Vector    │
│ • timestamp     │    │ [1024 numbers]   │
└─────────────────┘    └────────┬─────────┘
                                │
                                ▼
                       ┌────────────────┐
                       │ 5. FAISS Index │
                       │ • Fast search  │
                       │ • Cosine sim   │
                       └────────────────┘
```

---

## � Troubleshooting Common Issues

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

3. **Close other GPU programs** (games, video editing, etc.)

---

### Issue 2: "Connection to PostgreSQL failed"

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**

1. **Check if PostgreSQL is running:**
   ```powershell
   # Windows
   Get-Service postgresql*
   
   # Should show "Running"
   # If not, start it:
   Start-Service postgresql-x64-XX
   ```

2. **Verify credentials** in `config/indexing.yaml`:
   ```yaml
   database:
     postgres:
       password: "your_actual_password"  # Check this!
   ```

3. **Test connection manually:**
   ```bash
   psql -U postgres -d fashion_search
   # If this works, your credentials are correct
   ```

---

### Issue 3: "No images found in dataset"

**Error:**
```
ValueError: No images found in directory
```

**Solutions:**

1. **Check image folder path** in `config/indexing.yaml`:
   ```yaml
   dataset:
     image_dir: "../Dataset/Orignal_Dataset"  # Is this correct?
   ```

2. **Verify images exist:**
   ```powershell
   # Windows
   Get-ChildItem -Path "Dataset\Orignal_Dataset" -Filter *.jpg
   ```

3. **Check file formats:**
   - Supported: `.jpg`, `.jpeg`, `.png`
   - Not supported: `.gif`, `.bmp`, `.webp`

---

### Issue 4: "Model download fails"

**Error:**
```
HTTPError: 404 Client Error
```

**Solutions:**

1. **Check internet connection**

2. **Try downloading one model at a time**

3. **Clear Hugging Face cache:**
   ```powershell
   # Windows
   Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface
   ```

4. **Use proxy if needed:**
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com  # Linux/Mac
   $env:HF_ENDPOINT="https://hf-mirror.com"   # Windows PowerShell
   ```

---

### Issue 5: "Permission denied" or "Access denied"

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Run terminal as administrator** (Windows)

2. **Check file permissions:**
   ```powershell
   # Make sure you have read/write access to the folder
   ```

3. **Don't put project in protected folders** (C:\Program Files, etc.)

---

### Issue 6: "ModuleNotFoundError"

**Error:**
```
ModuleNotFoundError: No module named 'transformers'
```

**Solution:**

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

Or install specific package:
```bash
pip install transformers torch torchvision
```

---

### Issue 7: Pipeline runs but no output files

**Check:**

1. **Look for error messages** in the console
2. **Verify storage folder exists:**
   ```bash
   Indexing_Pipeline/storage/
   ```
3. **Check PostgreSQL for records:**
   ```sql
   SELECT COUNT(*) FROM fashion_images;
   ```

---

### Issue 8: Very slow processing

**Speed up tips:**

1. **Enable GPU** (if you have NVIDIA GPU):
   ```yaml
   models:
     img_to_text:
       device: "cuda"  # Change from "cpu"
   ```

2. **Increase batch size** (if GPU has memory):
   ```yaml
   dataset:
     batch_size: 8  # Try higher values
   ```

3. **Use SSD** instead of HDD for dataset

4. **Close background programs**

---

### Still Having Issues?

1. **Check full error message** - scroll up in terminal
2. **Run test script:**
   ```bash
   python Indexing_Pipeline/test_models_only.py
   ```
3. **Verify Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```
4. **Check logs** for detailed error information

---

## ⚙️ Advanced Configuration

### Batch Size Optimization

The `batch_size` parameter controls how many images process simultaneously:

```yaml
dataset:
  batch_size: 4  # Default
```

**How to choose:**

| GPU Memory | Recommended Batch Size |
|------------|------------------------|
| 4 GB       | 1-2                   |
| 6 GB       | 2-4                   |
| 8 GB       | 4-8                   |
| 12+ GB     | 8-16                  |
| CPU only   | 1-2                   |

**Rule of thumb:** Start small (2), then increase until you get memory errors, then reduce by 1.

---

### Model Device Selection

You can run different models on different devices:

```yaml
models:
  img_to_text:
    device: "cuda"  # Most memory-intensive - put on GPU
    
  text_normalization:
    device: "cuda"  # Medium - GPU if available
    
  embedding:
    device: "cpu"   # Lightweight - can use CPU to save GPU memory
```

**When to use CPU for some models:**
- Limited GPU memory (4-6 GB)
- Need GPU for other tasks
- Bottleneck is I/O, not computation

---

### Database Optimization

For large datasets (10,000+ images), optimize PostgreSQL:

```sql
-- Create index for faster queries
CREATE INDEX idx_image_path ON fashion_images(image_path);
CREATE INDEX idx_created_at ON fashion_images(created_at);
```

---

### FAISS Index Types

Current setup uses `IndexFlatIP` (exact search). For larger datasets:

```python
# In storage/faiss_writer.py, you can change to:
# IndexIVFFlat (faster but approximate)
# IndexHNSWFlat (balanced speed/accuracy)
```

See FAISS documentation for advanced indexing options.

---

### Dataset Organization Best Practices

```
Dataset/
├── Orignal_Dataset/          # Your images
│   ├── train/                # Main dataset
│   └── test/                 # Test images
│
├── processed/                # (optional) Store processed versions
└── metadata.csv              # (optional) Image annotations
```

---

### Logging Configuration

Edit `utils/logger.py` to change log level:

```python
logging.basicConfig(level=logging.INFO)  # Default
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

### Multi-GPU Support (Advanced)

To use multiple GPUs:

```python
# In model files, add:
device = torch.device("cuda:0")  # First GPU
device = torch.device("cuda:1")  # Second GPU
```

---

## 📊 Performance Benchmarks

### Processing Speed

**Hardware:** RTX 4060, 16GB RAM, SSD

| Dataset Size | CPU Time | GPU Time | Speedup |
|--------------|----------|----------|---------|
| 10 images    | 6 min    | 50 sec   | 7.2x    |
| 100 images   | 60 min   | 8.5 min  | 7.1x    |
| 500 images   | 5 hours  | 42 min   | 7.1x    |
| 1000 images  | 10 hours | 85 min   | 7.1x    |

### Accuracy Metrics

The pipeline doesn't evaluate accuracy (that's for the retrieval pipeline), but model quality:

- **Caption Quality:** Qwen2-VL is state-of-the-art vision-language model
- **Embedding Quality:** BGE models rank #1 on MTEB leaderboard
- **Search Relevance:** Depends on query normalization and reranking

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

### 3. Add More Images

Just add new images to your dataset folder and run the pipeline again:
- Existing images are skipped (no duplicates)
- Only new images are processed

### 4. Build a REST API

Integrate with your application using Flask/FastAPI:
```python
from Retrieval_Pipeline.retrieval_pipeline import search_fashion
results = search_fashion("red dress")
```

### 5. Fine-tune Models

For better accuracy on your specific fashion domain:
- Fine-tune Qwen2-VL on your image types
- Fine-tune BGE embeddings on fashion text
- Requires labeled training data

---

## 📚 Additional Resources

### Official Documentation

- **Transformers:** https://huggingface.co/docs/transformers
- **FAISS:** https://github.com/facebookresearch/faiss/wiki
- **PostgreSQL:** https://www.postgresql.org/docs/
- **PyTorch:** https://pytorch.org/docs/

### Model Information

- **Qwen2-VL:** https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct
- **Qwen2.5:** https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- **BGE Embeddings:** https://huggingface.co/BAAI/bge-large-en-v1.5

### Fashion Datasets

- **DeepFashion:** http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
- **Fashionpedia:** https://fashionpedia.github.io/home/index.html
- **Fashion Product Images:** https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset

---

## 💡 Tips for Best Results

1. **Start Small:** Test with 10-20 images first
2. **Use GPU:** Makes processing 7x faster
3. **High-Quality Images:** Clear, well-lit photos work best
4. **Consistent Naming:** Makes tracking easier
5. **Regular Backups:** Backup your FAISS index and database
6. **Monitor Resources:** Watch GPU memory and disk space
7. **Version Control:** Commit config changes to git

---

## 🤝 Need Help?

### Common Questions

**Q: How long does indexing take?**  
A: ~5 seconds per image on GPU, ~40 seconds on CPU

**Q: Can I index videos?**  
A: Not yet - extract frames first, then index as images

**Q: What's the maximum dataset size?**  
A: Limited by disk space - tested up to 10,000 images

**Q: Do I need all 3 models?**  
A: Yes - each serves a specific purpose in the pipeline

**Q: Can I use different models?**  
A: Yes, but requires code changes in `models/` folder

---

## 📝 Database Schema Reference

The `fashion_images` table structure:

```sql
CREATE TABLE fashion_images (
    id SERIAL PRIMARY KEY,              -- Auto-incrementing ID
    image_path TEXT NOT NULL,           -- Path to image file
    normalized_text TEXT NOT NULL,      -- Processed features
    created_at TIMESTAMP DEFAULT NOW()  -- When indexed
);
```

**Example record:**
```
id: 1
image_path: Dataset/Orignal_Dataset/shirt_001.jpg
normalized_text: shirt | blue | plaid | short sleeve | casual | ...
created_at: 2026-01-07 10:30:45
```

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

**Why numbers?** Computers can't understand "blue shirt", but they can calculate similarity between number vectors!

---

**🎉 You're all set! Run `python Indexing_Pipeline/run_indexing.py` to start indexing.**

---

*Last updated: January 2026*  
*Project: Fashion Search Engine*  
*Author: Prashant Takale*