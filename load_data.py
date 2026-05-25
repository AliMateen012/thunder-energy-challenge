#!/usr/bin/env python3
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sys

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thunder_energy',
    'user': 'postgres',
    'password': 'postgres'
}

def create_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def setup_schema(conn):
    try:
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        print("✓ Schema created successfully")
    except Exception as e:
        print(f"Error creating schema: {e}")
        conn.rollback()
        sys.exit(1)

def load_csv_to_db(conn, csv_path='Data_Engineering_Challenge (1).csv'):
    try:
        # Read CSV
        df = pd.read_csv(csv_path, encoding='latin1', sep=',', skipinitialspace=True)
        
        # Rename columns to match PostgreSQL schema (lowercase, underscore)
        df.columns = df.columns.str.strip()
        df.rename(columns={
            'Site Code': 'site_code',
            'Timestamp': 'timestamp',
            'Source Tag': 'source_tag',
            'Solar Output Current': 'solar_output_current',
            'Total Load Current': 'total_load_current',
            'Battery Total Current': 'battery_total_current',
            'Total Voltage': 'total_voltage'
        }, inplace=True)
        
        # Convert timestamp to timezone-aware
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Clean source_tag (remove extra spaces)
        df['source_tag'] = df['source_tag'].str.strip()
        
        print(f"✓ Read {len(df)} rows from CSV")
        print(f"✓ Columns: {list(df.columns)}")
        
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        df.to_sql('site_readings', engine, if_exists='append', index=False)
        print(f"✓ Loaded {len(df)} rows into database")
        
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM site_readings")
            count = cur.fetchone()[0]
            print(f"✓ Verification: {count} rows (expected 480)")
            return count == 480
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def main():
    print("=" * 60)
    print("Thunder Energy - Data Ingestion")
    print("=" * 60)
    
    print("\n1. Connecting to PostgreSQL...")
    conn = create_connection()
    
    print("\n2. Creating table schema...")
    setup_schema(conn)
    
    print("\n3. Loading CSV data...")
    success = load_csv_to_db(conn)
    
    if success:
        print("\n✅ Data ingestion completed successfully!")
        
        with conn.cursor() as cur:
            cur.execute("SELECT site_code, timestamp, source_tag FROM site_readings LIMIT 3")
            print("\n📊 Sample data:")
            for row in cur.fetchall():
                print(f"   {row}")
    else:
        print("\n❌ Data ingestion failed!")
    
    conn.close()

if __name__ == "__main__":
    main()