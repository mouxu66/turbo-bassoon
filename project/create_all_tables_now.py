import sqlite3
import os

DB_PATH = 'lol_items.db'
print(f"创建/修复数据库: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. 创建 items 表（根据你的代码需要的结构）
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    gold_total INTEGER DEFAULT 0,
    tags TEXT,
    stats TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ 创建 items 表")

# 2. 创建 matches 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT UNIQUE,
    game_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ 创建 matches 表")

# 3. 创建 analysis_cache 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS analysis_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ 创建 analysis_cache 表")

# 4. 查看现有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\n📊 数据库现有表:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  {table[0]}: {count} 条记录")

conn.commit()
conn.close()
print("\n🎉 数据库结构创建完成！")
