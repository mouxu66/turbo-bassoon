import sqlite3
import os

DB_PATH = 'lol_items.db'

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建 items 表（根据你 app.py 中的结构）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        gold_total INTEGER,
        tags TEXT,
        stats TEXT
    )
    ''')
    
    # 创建其他可能需要的表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT,
        game_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 已创建数据库表结构")

if __name__ == '__main__':
    create_tables()
