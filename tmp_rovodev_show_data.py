"""Show all data from the MSK Wellness database"""
import sqlite3
import json
from datetime import datetime

db_path = "backend/msk_chatbot.db"

def show_table_data(cursor, table_name):
    print(f"\n{'='*80}")
    print(f"TABLE: {table_name}")
    print('='*80)
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Get all rows
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f"Columns: {', '.join(columns)}")
    print(f"Row count: {len(rows)}\n")
    
    if rows:
        for i, row in enumerate(rows, 1):
            print(f"--- Row {i} ---")
            for col, val in zip(columns, row):
                # Pretty print JSON fields
                if col in ['performance_data', 'context'] and val:
                    try:
                        parsed = json.loads(val)
                        print(f"  {col}: {json.dumps(parsed, indent=4)}")
                    except:
                        print(f"  {col}: {val}")
                else:
                    print(f"  {col}: {val}")
            print()
    else:
        print("  (No data)")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    import os
    print("="*80)
    print("MSK WELLNESS DATABASE - ALL DATA")
    print("="*80)
    print(f"Database: {os.path.abspath(db_path)}")
    print(f"Tables: {', '.join(tables)}")
    
    # Show data from each table
    for table in tables:
        show_table_data(cursor, table)
    
    conn.close()
    print("\n" + "="*80)
    print("END OF DATA")
    print("="*80)
    
except Exception as e:
    print(f"Error: {e}")
