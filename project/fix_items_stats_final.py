import sqlite3

DB_PATH = 'lol_items.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查 matches 表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matches'")
if cursor.fetchone():
    print("✅ matches 表存在")
    cursor.execute("SELECT COUNT(*) FROM matches")
    count = cursor.fetchone()[0]
    print(f"   表中有 {count} 条记录")
    
    if count == 0:
        print("   提示：表为空，统计功能将显示0")
else:
    print("❌ matches 表不存在")
    print("   可以：1. 通过上传页面添加比赛数据")
    print("         2. 注释掉 items 页面中的统计查询")

conn.close()
