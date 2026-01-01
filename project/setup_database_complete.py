import sqlite3
import os

DB_PATH = 'lol_items.db'
print("=" * 50)
print("📦 开始设置英雄联盟数据分析数据库")
print("=" * 50)

# 如果数据库已存在，备份
if os.path.exists(DB_PATH):
    backup_name = f"{DB_PATH}.backup"
    import shutil
    shutil.copy2(DB_PATH, backup_name)
    print(f"📁 已备份原数据库到: {backup_name}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n1. 创建数据表...")

# 1. items 表（装备数据）
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
print("   ✅ items 表 - 装备数据")

# 2. matches 表（比赛数据）
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT UNIQUE,
    game_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("   ✅ matches 表 - 比赛数据")

# 3. analysis_cache 表（分析缓存）
cursor.execute('''
CREATE TABLE IF NOT EXISTS analysis_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("   ✅ analysis_cache 表 - 分析缓存")

print("\n2. 检查现有数据...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table_name in [t[0] for t in tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"   📊 {table_name:20} {count:4} 条记录")

conn.commit()

print("\n" + "=" * 50)
print("🎉 数据库结构创建完成！")
print("=" * 50)

# 显示数据库文件信息
import os
size_kb = os.path.getsize(DB_PATH) / 1024
print(f"\n📊 数据库文件: {DB_PATH}")
print(f"   大小: {size_kb:.1f} KB")
print(f"   表数量: {len(tables)}")

conn.close()
