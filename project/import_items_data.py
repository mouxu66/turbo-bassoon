import sqlite3
import csv
import os

DB_PATH = 'lol_items.db'
CSV_PATH = 'ItemTbl.csv'

def import_data():
    if not os.path.exists(CSV_PATH):
        print(f"❌ 数据文件 {CSV_PATH} 不存在")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 清空现有数据
    cursor.execute('DELETE FROM items')
    
    # 读取CSV并导入
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
            INSERT INTO items (name, description, gold_total, tags, stats)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                row.get('name', ''),
                row.get('description', ''),
                int(row.get('gold_total', 0) or 0),
                row.get('tags', ''),
                row.get('stats', '')
            ))
    
    conn.commit()
    
    # 统计导入的数据量
    cursor.execute('SELECT COUNT(*) FROM items')
    count = cursor.fetchone()[0]
    
    conn.close()
    print(f"✅ 已导入 {count} 条装备数据")

if __name__ == '__main__':
    import_data()
