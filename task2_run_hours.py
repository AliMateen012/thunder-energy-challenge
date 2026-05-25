#!/usr/bin/env python3
import psycopg2
import pandas as pd
import os

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thunder_energy',
    'user': 'postgres',
    'password': 'postgres'
}

def main():
    print("=" * 60)
    print("Task 2: Hourly Run Hours per Source")
    print("=" * 60)
    
    conn = psycopg2.connect(**DB_CONFIG)
    
    query = """
    SELECT site_code, 
           DATE_TRUNC('hour', timestamp) as hour_window,
           'DG' as source,
           ROUND((COUNT(*) * 3.0 / 60.0)::numeric, 3) as run_hours
    FROM site_readings
    WHERE source_tag ILIKE '%DG%'
    GROUP BY site_code, DATE_TRUNC('hour', timestamp)
    
    UNION ALL
    
    SELECT site_code, 
           DATE_TRUNC('hour', timestamp),
           'Solar',
           ROUND((COUNT(*) * 3.0 / 60.0)::numeric, 3)
    FROM site_readings
    WHERE source_tag ILIKE '%Solar%'
    GROUP BY site_code, DATE_TRUNC('hour', timestamp)
    
    UNION ALL
    
    SELECT site_code, 
           DATE_TRUNC('hour', timestamp),
           'Battery',
           ROUND((COUNT(*) * 3.0 / 60.0)::numeric, 3)
    FROM site_readings
    WHERE source_tag ILIKE '%Battery%'
    GROUP BY site_code, DATE_TRUNC('hour', timestamp)
    
    UNION ALL
    
    SELECT site_code, 
           DATE_TRUNC('hour', timestamp),
           'Mains',
           ROUND((COUNT(*) * 3.0 / 60.0)::numeric, 3)
    FROM site_readings
    WHERE source_tag ILIKE '%Mains%'
    GROUP BY site_code, DATE_TRUNC('hour', timestamp)
    
    ORDER BY hour_window, source
    """
    
    df = pd.read_sql(query, conn)
    os.makedirs('output', exist_ok=True)
    df.to_csv('output/run_hours.csv', index=False)
    
    print(f"\n✓ Run hours saved to output/run_hours.csv")
    print(f"✓ {len(df)} source-hour combinations")
    print("\n📊 First 10 rows:")
    print(df.head(10).to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    main()