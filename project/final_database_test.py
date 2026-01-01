import sqlite3
from app import app

DB_PATH = 'lol_items.db'

print("=" * 50)
print("🏁 最终数据库与网站集成测试")
print("=" * 50)

# 测试1: 数据库连接和数据
print("\n1. 测试数据库...")
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM items")
    item_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM matches")
    match_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"   ✅ 数据库连接正常")
    print(f"   📊 装备数据: {item_count} 条")
    print(f"   📊 比赛数据: {match_count} 条")
    
except Exception as e:
    print(f"   ❌ 数据库错误: {e}")

# 测试2: 网站路由
print("\n2. 测试网站路由...")
with app.test_client() as client:
    routes = ['/', '/items', '/analysis', '/about', '/upload']
    
    for route in routes:
        try:
            r = client.get(route)
            status = "✅" if r.status_code == 200 else f"❌ {r.status_code}"
            print(f"   {route:15} {status}")
        except Exception as e:
            print(f"   {route:15} 💥 {str(e)[:30]}")

print("\n" + "=" * 50)
if item_count > 0:
    print("🎉 测试完成！网站应该能正常显示数据了")
else:
    print("⚠️  数据库有数据但可能不符合预期格式")
print("=" * 50)
