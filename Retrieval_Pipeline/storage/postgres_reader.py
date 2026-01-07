"""
PostgreSQL Reader
"""
import psycopg2
from typing import List, Dict, Optional


class PostgresReader:
    """PostgreSQL reader for retrieving image metadata"""
    
    def __init__(self, config: dict):
        """
        Initialize PostgreSQL reader
        
        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.conn = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                dbname=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password']
            )
            print("✓ Connected to PostgreSQL database")
        except Exception as e:
            print(f"✗ Failed to connect to database: {e}")
            raise
    
    def get_images_by_ids(self, image_ids: List[int]) -> List[Dict]:
        """
        Retrieve image metadata by IDs
        
        Args:
            image_ids: List of image IDs
            
        Returns:
            List of dictionaries with image metadata
        """
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        
        # Query for images
        query = f"""
            SELECT image_id, image_path, normalized_text, created_at
            FROM {self.config['table_name']}
            WHERE image_id = ANY(%s)
        """
        
        cursor.execute(query, (image_ids,))
        results = cursor.fetchall()
        
        # Convert to list of dicts
        images = []
        for row in results:
            images.append({
                'id': row[0],
                'image_path': row[1],
                'normalized_text': row[2],
                'created_at': row[3]
            })
        
        cursor.close()
        return images
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
