# Indexing Pipeline - Utility Scripts

This folder contains utility scripts for database and model testing.

## Scripts

### `clear_db.py`
Clears all processed data from PostgreSQL database and deletes FAISS index files.

**Usage:**
```bash
python scripts/clear_db.py
```

**What it does:**
- Truncates the `fashion_images` table
- Deletes `storage/faiss_index.bin`
- Deletes `storage/faiss_index_ids.npy`

---

### `setup_database.py`
Creates the PostgreSQL database if it doesn't exist.

**Usage:**
```bash
python scripts/setup_database.py
```

**What it does:**
- Creates `fashion_search` database
- Uses default PostgreSQL connection settings

---

### `test_models_only.py`
Tests AI models without database connection - useful for debugging model issues.

**Usage:**
```bash
python scripts/test_models_only.py
```

**What it does:**
- Loads all 3 AI models (Image-to-Text, Text Normalization, Embedding)
- Processes a few test images
- Shows model outputs without storing to database
---

## Main Indexing Pipeline

To run the main indexing pipeline, use:
```bash
python run_indexing.py
```
(from the Indexing_Pipeline directory)
