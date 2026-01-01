import sqlite3

DB_PATH = 'lol_items.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 创建 matches 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT,
    game_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 创建其他可能缺失的表
cursor.execute('''
CREATE TABLE IF NOT EXISTS analysis_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# 检查现有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("现有表:", [t[0] for t in tables])

conn.close()
print("✅ 已创建缺失的数据库表")
