import sqlite3
import csv
import os

DB_PATH = 'lol_items.db'
CSV_PATH = 'ItemTbl.csv'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 清空现有数据（可选）
cursor.execute("DELETE FROM items")

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        cursor.execute('''
        INSERT INTO items (name, description, gold_total, tags, stats)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('name', f'装备{i}'),
            row.get('description', ''),
            int(row.get('gold_total', 0) or 0),
            row.get('tags', ''),
            row.get('stats', '')
        ))
        if i % 50 == 0:
            print(f"已导入 {i} 条...")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM items")
total = cursor.fetchone()[0]
conn.close()

print(f"✅ 成功导入 {total} 条装备数据到数据库")
