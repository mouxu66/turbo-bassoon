import sqlite3
import csv
import os
import re

print("🚀 开始完整数据导入...")
print("=" * 60)

db_path = '/home/mouxu/lol_items.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. 清空现有数据
cursor.execute("DELETE FROM item")
cursor.execute("DELETE FROM items")
print("✅ 清空旧数据")

# 2. 读取ItemTbl.csv（有746个物品）
item_data = []
if os.path.exists('ItemTbl.csv'):
    print("📥 读取ItemTbl.csv...")
    with open('ItemTbl.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row['ItemID'].strip()
            item_name = row['ItemName'].strip()
            
            # 清理HTML标签
            if '<' in item_name:
                item_name = re.sub(r'<[^>]+>', '', item_name)
            
            if item_name:  # 只处理有名称的物品
                item_data.append({
                    'id': item_id,
                    'name': item_name
                })
    
    print(f"  找到 {len(item_data)} 个物品")
else:
    print("❌ ItemTbl.csv 不存在")
    item_data = []

# 3. 读取LOL_items_stats.csv获取属性
items_stats = {}
if os.path.exists('LOL_items_stats.csv'):
    print("📥 读取LOL_items_stats.csv...")
    with open('LOL_items_stats.csv', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\\n')
        
        if len(lines) > 1:
            headers = [h.strip() for h in lines[0].split(';')]
            
            for line in lines[1:]:
                values = [v.strip() for v in line.split(';')]
                if len(values) < 2:
                    continue
                
                item_name = values[0]
                item_info = {}
                
                for i, header in enumerate(headers):
                    if i < len(values):
                        value = values[i]
                        if value and value not in ['...', '', '.']:
                            item_info[header.lower()] = value
                
                items_stats[item_name] = item_info
    
    print(f"  读取了 {len(items_stats)} 个物品的属性")
else:
    print("❌ LOL_items_stats.csv 不存在")
    items_stats = {}

# 4. 导入数据到item表
print("\\n💾 导入数据到item表...")
imported = 0
for item in item_data:
    stats = items_stats.get(item['name'], {})
    
    # 确定物品类型
    item_type = 'other'
    name_lower = item['name'].lower()
    
    if stats.get('ad'):
        try:
            if int(stats['ad']) > 0:
                item_type = 'attack'
        except:
            pass
    elif stats.get('ap'):
        try:
            if int(stats['ap']) > 0:
                item_type = 'spell'
        except:
            pass
    elif stats.get('health') or stats.get('armor') or stats.get('mr'):
        item_type = 'defense'
    elif 'boots' in name_lower:
        item_type = 'boots'
    
    try:
        cursor.execute('''
        INSERT INTO item 
        (item_id, name, display_name, cost, sell, ad, attack_speed, crit, 
         lifesteal, armor_pen, ap, ability_haste, mana, mp5, magic_pen,
         health, armor, mr, hp5, ms, omnivamp, shield_power, description,
         effect, item_type, maps, tags, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['id'],                    # item_id
            item['name'],                  # name
            item['name'],                  # display_name（暂时用name）
            stats.get('cost'),            # cost
            stats.get('sell'),            # sell
            stats.get('ad'),              # ad
            stats.get('as'),              # attack_speed
            stats.get('crit'),            # crit
            stats.get('ls'),              # lifesteal
            stats.get('apen'),            # armor_pen
            stats.get('ap'),              # ap
            stats.get('ah'),              # ability_haste
            stats.get('mana'),            # mana
            stats.get('mp5'),             # mp5
            stats.get('mpen'),            # magic_pen
            stats.get('health'),          # health
            stats.get('armor'),           # armor
            stats.get('mr'),               # mr
            stats.get('hp5'),             # hp5
            stats.get('ms'),               # ms
            stats.get('ovamp'),           # omnivamp
            stats.get('hsp'),              # shield_power
            None,                          # description
            None,                          # effect
            item_type,                    # item_type
            stats.get('maps', 'All'),     # maps
            None,                          # tags
            None                           # image
        ))
        imported += 1
        
        if imported % 100 == 0:
            print(f"  已导入 {imported} 个...")
            
    except Exception as e:
        # 跳过错误，继续导入
        pass

conn.commit()

# 5. 也导入到items表（保持一致性）
print("\\n📋 复制数据到items表...")
cursor.execute("INSERT INTO items SELECT * FROM item")

# 6. 验证结果
cursor.execute("SELECT COUNT(*) FROM item")
item_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM items")
items_count = cursor.fetchone()[0]

print(f"\\n✅ 导入完成!")
print(f"   item表: {item_count} 条记录")
print(f"   items表: {items_count} 条记录")

# 显示一些示例
cursor.execute("SELECT name, cost FROM item WHERE cost IS NOT NULL ORDER BY cost DESC LIMIT 3")
expensive = cursor.fetchall()
cursor.execute("SELECT name, cost FROM item WHERE cost IS NOT NULL ORDER BY cost ASC LIMIT 3")
cheap = cursor.fetchall()

print("\\n💰 最贵的3个装备:")
for name, cost in expensive:
    print(f"   {name}: {cost}金币")

print("\\n💸 最便宜的3个装备:")
for name, cost in cheap:
    print(f"   {name}: {cost}金币")

conn.close()
print("=" * 60)
