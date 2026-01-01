import sqlite3
import csv
import os

DB_PATH = 'lol_items.db'
CSV_FILE = 'ItemTbl.csv'

if not os.path.exists(CSV_FILE):
    print(f"❌ 找不到文件: {CSV_FILE}")
    print("请先确认文件是否存在，或使用其他文件名")
    exit(1)

print(f"开始从 {CSV_FILE} 导入数据到数据库...")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 先清空现有数据（可选）
cursor.execute("DELETE FROM items")
print("已清空原有装备数据")

# 读取CSV文件
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    # 尝试自动检测分隔符和编码
    sample = f.read(1024)
    f.seek(0)
    
    # 判断分隔符
    if ',' in sample:
        delimiter = ','
    elif ';' in sample:
        delimiter = ';'
    elif '\t' in sample:
        delimiter = '\t'
    else:
        delimiter = ','
    
    print(f"检测到分隔符: {repr(delimiter)}")
    
    reader = csv.DictReader(f, delimiter=delimiter)
    fieldnames = reader.fieldnames
    print(f"CSV列名: {fieldnames}")
    
    imported = 0
    for row in reader:
        # 根据CSV列名映射到数据库字段
        name = row.get('name') or row.get('Name') or row.get('ITEMNAME') or f"装备{imported+1}"
        description = row.get('description') or row.get('Description') or ''
        
        # 尝试解析价格/金币
        gold_str = row.get('gold_total') or row.get('Gold') or row.get('price') or '0'
        try:
            gold_total = int(gold_str)
        except:
            gold_total = 0
        
        tags = row.get('tags') or row.get('Tags') or ''
        stats = row.get('stats') or row.get('Stats') or ''
        
        cursor.execute('''
        INSERT INTO items (name, description, gold_total, tags, stats)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, description, gold_total, tags, stats))
        
        imported += 1
        if imported % 50 == 0:
            print(f"已导入 {imported} 条...")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM items")
total = cursor.fetchone()[0]

conn.close()

print(f"\n✅ 导入完成！")
print(f"   从 {CSV_FILE} 导入 {imported} 条装备数据")
print(f"   数据库中共有 {total} 条装备记录")
