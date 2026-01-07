"""
Store image_id, path, normalized text in PostgreSQL
"""
import psycopg2
from psycopg2.extras import execute_batch
from typing import List, Tuple, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PostgresWriter:
    """Handle PostgreSQL database operations"""
    
    def __init__(self, config: dict):
        """
        Initialize PostgreSQL connection
        
        Args:
            config: Database configuration dict
        """
        self.config = config
        self.conn = None
        self.cursor = None
        self.table_name = config.get('table_name', 'fashion_images')
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                dbname=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password']
            )
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def create_table(self, schema_file: str):
        """
        Create table from schema file
        
        Args:
            schema_file: Path to SQL schema file
        """
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
            self.cursor.execute(schema)
            self.conn.commit()
            logger.info("Database table created/verified")
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            self.conn.rollback()
            raise
    
    def insert_record(self, image_path: str, normalized_text: str) -> Optional[int]:
        """
        Insert single record
        
        Args:
            image_path: Path to image file
            normalized_text: Normalized text description
        
        Returns:
            image_id of inserted record
        """
        try:
            query = f"""
                INSERT INTO {self.table_name} (image_path, normalized_text)
                VALUES (%s, %s)
                ON CONFLICT (image_path) DO UPDATE
                SET normalized_text = EXCLUDED.normalized_text
                RETURNING image_id
            """
            self.cursor.execute(query, (image_path, normalized_text))
            image_id = self.cursor.fetchone()[0]
            self.conn.commit()
            logger.debug(f"Inserted record with image_id: {image_id}")
            return image_id
        except Exception as e:
            logger.error(f"Failed to insert record: {e}")
            self.conn.rollback()
            return None
    
    def insert_batch(self, records: List[Tuple[str, str]]) -> List[int]:
        """
        Insert batch of records
        
        Args:
            records: List of (image_path, normalized_text) tuples
        
        Returns:
            List of image_ids
        """
        image_ids = []
        try:
            query = f"""
                INSERT INTO {self.table_name} (image_path, normalized_text)
                VALUES (%s, %s)
                ON CONFLICT (image_path) DO UPDATE
                SET normalized_text = EXCLUDED.normalized_text
                RETURNING image_id
            """
            for record in records:
                self.cursor.execute(query, record)
                image_id = self.cursor.fetchone()[0]
                image_ids.append(image_id)
            
            self.conn.commit()
            logger.info(f"Inserted {len(records)} records")
            return image_ids
        except Exception as e:
            logger.error(f"Failed to insert batch: {e}")
            self.conn.rollback()
            return []
    
    def get_image_id(self, image_path: str) -> Optional[int]:
        """
        Get image_id for given image_path
        
        Args:
            image_path: Path to image
        
        Returns:
            image_id or None
        """
        try:
            query = f"SELECT image_id FROM {self.table_name} WHERE image_path = %s"
            self.cursor.execute(query, (image_path,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Failed to get image_id: {e}")
            return None
    
    def get_all_image_paths(self) -> List[str]:
        """
        Get all image paths already in database
        
        Returns:
            List of image paths
        """
        try:
            query = f"SELECT image_path FROM {self.table_name}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            logger.error(f"Failed to get image paths: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")
