"""
Setup PostgreSQL database for fashion search
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to default postgres database
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",  # Connect to default database
        user="postgres",
        password="123"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'fashion_search'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("CREATE DATABASE fashion_search")
        print("✓ Database 'fashion_search' created successfully!")
    else:
        print("✓ Database 'fashion_search' already exists")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure:")
    print("1. PostgreSQL is running")
    print("2. Password is correct (current: 1234)")
    print("3. User 'postgres' has permissions")
