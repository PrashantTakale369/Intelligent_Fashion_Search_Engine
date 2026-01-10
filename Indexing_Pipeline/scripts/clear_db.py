"""
Clear Database Script

Clears all records from the fashion_images table to start fresh with new dataset
"""
import psycopg2
import os

def clear_database():
    """Clear all records from fashion_images table and delete FAISS files"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="fashion_search",
            user="postgres",
            password="123"
        )
        
        cursor = conn.cursor()
        
        # Truncate the table
        cursor.execute("TRUNCATE TABLE fashion_images CASCADE;")
        conn.commit()
        
        # Get count
        cursor.execute("SELECT COUNT(*) FROM fashion_images;")
        count = cursor.fetchone()[0]
        
        print(f"✓ Database cleared successfully")
        print(f"✓ Current records: {count}")
        
        cursor.close()
        conn.close()
        
        # Delete FAISS files
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        faiss_index = os.path.join(parent_dir, 'storage', 'faiss_index.bin')
        faiss_ids = os.path.join(parent_dir, 'storage', 'faiss_index_ids.npy')
        
        if os.path.exists(faiss_index):
            os.remove(faiss_index)
            print(f"✓ Deleted FAISS index file")
        
        if os.path.exists(faiss_ids):
            os.remove(faiss_ids)
            print(f"✓ Deleted FAISS IDs file")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clear_database()
