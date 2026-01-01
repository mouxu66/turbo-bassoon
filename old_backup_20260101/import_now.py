import sqlite3
import csv
import os
import re

print("=" * 60)
print("🚀 LOL装备数据导入程序")
print("=" * 60)

# 数据库路径
DB_PATH = '/home/mouxu/lol_items.db'

def clean_name(name):
    """清理物品名称"""
    if not name:
        return ""
    # 移除HTML标签
    name = re.sub(r'<[^>]+>', '', name)
    # 移除多余空格
    name = name.strip()
    return name

def import_data():
    """导入数据到数据库"""
    
    # 1. 创建/重置数据库
    print("1. 准备数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 删除旧表
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS item')
    
    # 创建新表
    cursor.execute('''
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost INTEGER,
        sell_price INTEGER,
        ad INTEGER,
        ap INTEGER,
        health INTEGER,
        armor INTEGER,
        magic_resist INTEGER,
        attack_speed REAL,
        crit_chance REAL,
        lifesteal REAL,
        ability_haste INTEGER,
        mana INTEGER,
        move_speed INTEGER,
        item_type TEXT
    )
    ''')
    
    print("✅ 数据库表已创建")
    
    # 2. 添加测试数据（先用这个测试网站能否显示）
    print("\n2. 导入测试数据...")
    
    test_items = [
        # 名称, 价格, AD, AP, 生命, 护甲, 魔抗, 攻速, 暴击, 吸血, 法力, 移速, 类型
        ('无尽之刃', 3400, 70, 0, 0, 0, 0, 0, 0.20, 0, 0, 0, 'attack'),
        ('灭世者的死亡之帽', 3600, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('日炎圣盾', 2800, 0, 0, 450, 50, 0, 0, 0, 0, 0, 0, 'defense'),
        ('破败王者之刃', 3300, 40, 0, 0, 0, 0, 0.25, 0, 0.08, 0, 0, 'attack'),
        ('卢登的激荡', 3200, 0, 80, 0, 0, 0, 0, 0, 0, 600, 0, 'spell'),
        ('狂徒铠甲', 3000, 0, 0, 800, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('疾行之靴', 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 'boots'),
        ('法师之靴', 1100, 0, 18, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('明朗之靴', 950, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('忍者足具', 1100, 0, 0, 0, 20, 0, 0, 0, 0, 0, 45, 'boots'),
        ('水银之靴', 1100, 0, 0, 0, 0, 25, 0, 0, 0, 0, 45, 'boots'),
        ('锁子甲', 800, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 'defense'),
        ('负极斗篷', 900, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 'defense'),
        ('暴风大剑', 1300, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('无用大棒', 1250, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('巨人腰带', 1000, 0, 0, 350, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('灵巧披风', 600, 0, 0, 0, 0, 0, 0, 0.15, 0, 0, 0, 'attack'),
        ('抗魔斗篷', 450, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 'defense'),
        ('长剑', 350, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('增幅典籍', 435, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红水晶', 400, 0, 0, 150, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('布甲', 300, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 'defense'),
        ('短剑', 300, 0, 0, 0, 0, 0, 0.12, 0, 0, 0, 0, 'attack'),
        ('蓝水晶', 350, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('治疗宝珠', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('吸血鬼节杖', 900, 15, 0, 0, 0, 0, 0, 0, 0.07, 0, 0, 'attack'),
        ('恶魔法典', 900, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('燃烧宝石', 800, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('考尔菲德的战锤', 1100, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('耀光', 700, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('净蚀', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('海克斯科技发电机', 1050, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('死刑宣告', 800, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('禁忌雕像', 550, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('冰川护甲', 900, 0, 0, 0, 20, 0, 0, 0, 0, 250, 0, 'defense'),
        ('猛禽斗篷', 900, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 'defense'),
        ('紫雨林之拳', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('以太精魂', 850, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('蓝惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('监视守卫', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('控制守卫', 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('生命药水', 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('复用型药水', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('腐败药水', 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('鞋子', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('速度之靴', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('多兰之盾', 450, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 'starter'),
        ('多兰之戒', 400, 0, 15, 0, 0, 0, 0, 0, 0, 70, 0, 'starter'),
        ('多兰之刃', 450, 8, 0, 80, 0, 0, 0, 0, 0.025, 0, 0, 'starter')
    ]
    
    imported = 0
    for item in test_items:
        cursor.execute('''
        INSERT INTO items 
        (name, cost, ad, ap, health, armor, magic_resist, attack_speed, 
         crit_chance, lifesteal, mana, move_speed, item_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)
        imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ 成功导入 {imported} 个装备")
    return imported

def verify_import():
    """验证导入结果"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT name, cost, item_type FROM items LIMIT 10")
        samples = cursor.fetchall()
        
        conn.close()
        
        print(f"\n📊 验证结果:")
        print(f"   数据库记录数: {count}")
        print(f"   示例装备:")
        for name, cost, item_type in samples:
            print(f"     - {name:20} | {cost:4}金币 | {item_type}")
        
        return count
    except Exception as e:
        print(f"验证失败: {e}")
        return 0

# 主程序
if __name__ == '__main__':
    print(f"数据库路径: {DB_PATH}")
    print(f"文件存在: {os.path.exists(DB_PATH)}")
    
    imported_count = import_data()
    final_count = verify_import()
    
    print("\n" + "=" * 60)
    if final_count > 0:
        print(f"🎉 导入成功！数据库中有 {final_count} 件装备")
        print("现在可以:")
        print("1. 修改WSGI文件指向 final_app_final_fixed.py")
        print("2. 点击Reload重新加载网站")
        print("3. 访问 http://mouxu.pythonanywhere.com")
    else:
        print("❌ 导入失败，请检查错误信息")
    print("=" * 60)
EOFcd /home/mouxu
cat > import_now.py << 'EOF'
import sqlite3
import csv
import os
import re

print("=" * 60)
print("🚀 LOL装备数据导入程序")
print("=" * 60)

# 数据库路径
DB_PATH = '/home/mouxu/lol_items.db'

def clean_name(name):
    """清理物品名称"""
    if not name:
        return ""
    # 移除HTML标签
    name = re.sub(r'<[^>]+>', '', name)
    # 移除多余空格
    name = name.strip()
    return name

def import_data():
    """导入数据到数据库"""
    
    # 1. 创建/重置数据库
    print("1. 准备数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 删除旧表
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS item')
    
    # 创建新表
    cursor.execute('''
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost INTEGER,
        sell_price INTEGER,
        ad INTEGER,
        ap INTEGER,
        health INTEGER,
        armor INTEGER,
        magic_resist INTEGER,
        attack_speed REAL,
        crit_chance REAL,
        lifesteal REAL,
        ability_haste INTEGER,
        mana INTEGER,
        move_speed INTEGER,
        item_type TEXT
    )
    ''')
    
    print("✅ 数据库表已创建")
    
    # 2. 添加测试数据（先用这个测试网站能否显示）
    print("\n2. 导入测试数据...")
    
    test_items = [
        # 名称, 价格, AD, AP, 生命, 护甲, 魔抗, 攻速, 暴击, 吸血, 法力, 移速, 类型
        ('无尽之刃', 3400, 70, 0, 0, 0, 0, 0, 0.20, 0, 0, 0, 'attack'),
        ('灭世者的死亡之帽', 3600, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('日炎圣盾', 2800, 0, 0, 450, 50, 0, 0, 0, 0, 0, 0, 'defense'),
        ('破败王者之刃', 3300, 40, 0, 0, 0, 0, 0.25, 0, 0.08, 0, 0, 'attack'),
        ('卢登的激荡', 3200, 0, 80, 0, 0, 0, 0, 0, 0, 600, 0, 'spell'),
        ('狂徒铠甲', 3000, 0, 0, 800, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('疾行之靴', 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 'boots'),
        ('法师之靴', 1100, 0, 18, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('明朗之靴', 950, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('忍者足具', 1100, 0, 0, 0, 20, 0, 0, 0, 0, 0, 45, 'boots'),
        ('水银之靴', 1100, 0, 0, 0, 0, 25, 0, 0, 0, 0, 45, 'boots'),
        ('锁子甲', 800, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 'defense'),
        ('负极斗篷', 900, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 'defense'),
        ('暴风大剑', 1300, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('无用大棒', 1250, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('巨人腰带', 1000, 0, 0, 350, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('灵巧披风', 600, 0, 0, 0, 0, 0, 0, 0.15, 0, 0, 0, 'attack'),
        ('抗魔斗篷', 450, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 'defense'),
        ('长剑', 350, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('增幅典籍', 435, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红水晶', 400, 0, 0, 150, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('布甲', 300, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 'defense'),
        ('短剑', 300, 0, 0, 0, 0, 0, 0.12, 0, 0, 0, 0, 'attack'),
        ('蓝水晶', 350, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('治疗宝珠', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('吸血鬼节杖', 900, 15, 0, 0, 0, 0, 0, 0, 0.07, 0, 0, 'attack'),
        ('恶魔法典', 900, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('燃烧宝石', 800, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('考尔菲德的战锤', 1100, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('耀光', 700, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('净蚀', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('海克斯科技发电机', 1050, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('死刑宣告', 800, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('禁忌雕像', 550, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('冰川护甲', 900, 0, 0, 0, 20, 0, 0, 0, 0, 250, 0, 'defense'),
        ('猛禽斗篷', 900, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 'defense'),
        ('紫雨林之拳', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('以太精魂', 850, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('蓝惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('监视守卫', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('控制守卫', 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('生命药水', 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('复用型药水', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('腐败药水', 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('鞋子', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('速度之靴', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('多兰之盾', 450, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 'starter'),
        ('多兰之戒', 400, 0, 15, 0, 0, 0, 0, 0, 0, 70, 0, 'starter'),
        ('多兰之刃', 450, 8, 0, 80, 0, 0, 0, 0, 0.025, 0, 0, 'starter')
    ]
    
    imported = 0
    for item in test_items:
        cursor.execute('''
        INSERT INTO items 
        (name, cost, ad, ap, health, armor, magic_resist, attack_speed, 
         crit_chance, lifesteal, mana, move_speed, item_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)
        imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ 成功导入 {imported} 个装备")
    return imported

def verify_import():
    """验证导入结果"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT name, cost, item_type FROM items LIMIT 10")
        samples = cursor.fetchall()
        
        conn.close()
        
        print(f"\n📊 验证结果:")
        print(f"   数据库记录数: {count}")
        print(f"   示例装备:")
        for name, cost, item_type in samples:
            print(f"     - {name:20} | {cost:4}金币 | {item_type}")
        
        return count
    except Exception as e:
        print(f"验证失败: {e}")
        return 0

# 主程序
if __name__ == '__main__':
    print(f"数据库路径: {DB_PATH}")
    print(f"文件存在: {os.path.exists(DB_PATH)}")
    
    imported_count = import_data()
    final_count = verify_import()
    
    print("\n" + "=" * 60)
    if final_count > 0:
        print(f"🎉 导入成功！数据库中有 {final_count} 件装备")
        print("现在可以:")
        print("1. 修改WSGI文件指向 final_app_final_fixed.py")
        print("2. 点击Reload重新加载网站")
        print("3. 访问 http://mouxu.pythonanywhere.com")
    else:
        print("❌ 导入失败，请检查错误信息")
    print("=" * 60)
cd /home/mouxu
cat > import_now.py << 'EOF'
import sqlite3
import csv
import os
import re

print("=" * 60)
print("🚀 LOL装备数据导入程序")
print("=" * 60)

# 数据库路径
DB_PATH = '/home/mouxu/lol_items.db'

def clean_name(name):
    """清理物品名称"""
    if not name:
        return ""
    # 移除HTML标签
    name = re.sub(r'<[^>]+>', '', name)
    # 移除多余空格
    name = name.strip()
    return name

def import_data():
    """导入数据到数据库"""
    
    # 1. 创建/重置数据库
    print("1. 准备数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 删除旧表
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS item')
    
    # 创建新表
    cursor.execute('''
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost INTEGER,
        sell_price INTEGER,
        ad INTEGER,
        ap INTEGER,
        health INTEGER,
        armor INTEGER,
        magic_resist INTEGER,
        attack_speed REAL,
        crit_chance REAL,
        lifesteal REAL,
        ability_haste INTEGER,
        mana INTEGER,
        move_speed INTEGER,
        item_type TEXT
    )
    ''')
    
    print("✅ 数据库表已创建")
    
    # 2. 添加测试数据（先用这个测试网站能否显示）
    print("\n2. 导入测试数据...")
    
    test_items = [
        # 名称, 价格, AD, AP, 生命, 护甲, 魔抗, 攻速, 暴击, 吸血, 法力, 移速, 类型
        ('无尽之刃', 3400, 70, 0, 0, 0, 0, 0, 0.20, 0, 0, 0, 'attack'),
        ('灭世者的死亡之帽', 3600, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('日炎圣盾', 2800, 0, 0, 450, 50, 0, 0, 0, 0, 0, 0, 'defense'),
        ('破败王者之刃', 3300, 40, 0, 0, 0, 0, 0.25, 0, 0.08, 0, 0, 'attack'),
        ('卢登的激荡', 3200, 0, 80, 0, 0, 0, 0, 0, 0, 600, 0, 'spell'),
        ('狂徒铠甲', 3000, 0, 0, 800, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('疾行之靴', 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 'boots'),
        ('法师之靴', 1100, 0, 18, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('明朗之靴', 950, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 'boots'),
        ('忍者足具', 1100, 0, 0, 0, 20, 0, 0, 0, 0, 0, 45, 'boots'),
        ('水银之靴', 1100, 0, 0, 0, 0, 25, 0, 0, 0, 0, 45, 'boots'),
        ('锁子甲', 800, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 'defense'),
        ('负极斗篷', 900, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 'defense'),
        ('暴风大剑', 1300, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('无用大棒', 1250, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('巨人腰带', 1000, 0, 0, 350, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('灵巧披风', 600, 0, 0, 0, 0, 0, 0, 0.15, 0, 0, 0, 'attack'),
        ('抗魔斗篷', 450, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 'defense'),
        ('长剑', 350, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('增幅典籍', 435, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红水晶', 400, 0, 0, 150, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('布甲', 300, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 'defense'),
        ('短剑', 300, 0, 0, 0, 0, 0, 0.12, 0, 0, 0, 0, 'attack'),
        ('蓝水晶', 350, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('治疗宝珠', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('吸血鬼节杖', 900, 15, 0, 0, 0, 0, 0, 0, 0.07, 0, 0, 'attack'),
        ('恶魔法典', 900, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('燃烧宝石', 800, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'defense'),
        ('考尔菲德的战锤', 1100, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('耀光', 700, 0, 0, 0, 0, 0, 0, 0, 0, 250, 0, 'spell'),
        ('净蚀', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('海克斯科技发电机', 1050, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('死刑宣告', 800, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('禁忌雕像', 550, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('冰川护甲', 900, 0, 0, 0, 20, 0, 0, 0, 0, 250, 0, 'defense'),
        ('猛禽斗篷', 900, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 'defense'),
        ('紫雨林之拳', 1100, 15, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'attack'),
        ('以太精魂', 850, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 'spell'),
        ('红惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('蓝惩戒', 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('监视守卫', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('控制守卫', 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'other'),
        ('生命药水', 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('复用型药水', 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('腐败药水', 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'consumable'),
        ('鞋子', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('速度之靴', 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 'boots'),
        ('多兰之盾', 450, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 'starter'),
        ('多兰之戒', 400, 0, 15, 0, 0, 0, 0, 0, 0, 70, 0, 'starter'),
        ('多兰之刃', 450, 8, 0, 80, 0, 0, 0, 0, 0.025, 0, 0, 'starter')
    ]
    
    imported = 0
    for item in test_items:
        cursor.execute('''
        INSERT INTO items 
        (name, cost, ad, ap, health, armor, magic_resist, attack_speed, 
         crit_chance, lifesteal, mana, move_speed, item_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)
        imported += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ 成功导入 {imported} 个装备")
    return imported

def verify_import():
    """验证导入结果"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT name, cost, item_type FROM items LIMIT 10")
        samples = cursor.fetchall()
        
        conn.close()
        
        print(f"\n📊 验证结果:")
        print(f"   数据库记录数: {count}")
        print(f"   示例装备:")
        for name, cost, item_type in samples:
            print(f"     - {name:20} | {cost:4}金币 | {item_type}")
        
        return count
    except Exception as e:
        print(f"验证失败: {e}")
        return 0

# 主程序
if __name__ == '__main__':
    print(f"数据库路径: {DB_PATH}")
    print(f"文件存在: {os.path.exists(DB_PATH)}")
    
    imported_count = import_data()
    final_count = verify_import()
    
    print("\n" + "=" * 60)
    if final_count > 0:
        print(f"🎉 导入成功！数据库中有 {final_count} 件装备")
        print("现在可以:")
        print("1. 修改WSGI文件指向 final_app_final_fixed.py")
        print("2. 点击Reload重新加载网站")
        print("3. 访问 http://mouxu.pythonanywhere.com")
    else:
        print("❌ 导入失败，请检查错误信息")
    print("=" * 60)
