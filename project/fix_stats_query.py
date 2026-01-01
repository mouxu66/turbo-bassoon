import sqlite3

DB_PATH = 'lol_items.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查 matches 表的结构
cursor.execute("PRAGMA table_info(matches)")
columns = cursor.fetchall()
print("matches 表结构:", columns)

# 如果表是空的，添加一些示例数据或调整查询
cursor.execute("SELECT COUNT(*) FROM matches")
count = cursor.fetchone()[0]
print(f"matches 表现有数据: {count} 条")

conn.close()

if count == 0:
    print("提示: matches 表为空，统计查询可能返回0或错误")
    print("你可以通过上传比赛数据来填充此表")
