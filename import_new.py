#!/usr/bin/env python3
"""
英雄联盟装备数据导入脚本
"""
import sqlite3
import json
import os
import time
import requests
from pathlib import Path

def init_database():
    """初始化数据库"""
    db_path = Path(__file__).parent / 'lol_items.db'
    
    # 删除旧数据库（可选）
    if db_path.exists():
        backup_path = db_path.with_suffix(f'.backup.{int(time.time())}.db')
        db_path.rename(backup_path)
        print(f"📁 已备份旧数据库: {backup_path.name}")
    
    # 创建新数据库
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 创建items表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        plaintext TEXT,
        description TEXT,
        gold_total INTEGER,
        gold_base INTEGER,
        gold_sell INTEGER,
        tags TEXT,
        stats TEXT,
        depth INTEGER,
        into_items TEXT,
        from_items TEXT,
        maps TEXT,
        image TEXT,
        category TEXT,
        version TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX idx_name ON items(name)')
    cursor.execute('CREATE INDEX idx_cost ON items(gold_total)')
    cursor.execute('CREATE INDEX idx_category ON items(category)')
    
    conn.commit()
    print("✅ 数据库结构创建完成")
    return conn

def insert_sample_data(conn):
    """插入示例数据（因为没有Riot API Key）"""
    cursor = conn.cursor()
    
    sample_items = [
        {
            'item_id': 1001,
            'name': '多兰之刃',
            'plaintext': '提供攻击力和生命偷取',
            'description': '+8攻击力 +80生命值 +2.5%生命偷取',
            'gold_total': 450,
            'gold_base': 450,
            'gold_sell': 180,
            'tags': '起始,攻击',
            'stats': '{"attack_damage": 8, "health": 80, "life_steal": 0.025}',
            'depth': 1,
            'category': '起始装备',
            'version': '13.24'
        },
        {
            'item_id': 3078,
            'name': '三相之力',
            'plaintext': '提供全面的属性加成',
            'description': '+20攻击力 +30%攻击速度 +300生命值 +200法力值 +20技能急速',
            'gold_total': 3333,
            'gold_base': 333,
            'gold_sell': 1333,
            'tags': '攻击,生命,法力,冷却缩减',
            'stats': '{"attack_damage": 20, "attack_speed": 0.3, "health": 300, "mana": 200, "ability_haste": 20}',
            'depth': 3,
            'category': '神话装备',
            'version': '13.24'
        },
        {
            'item_id': 3089,
            'name': '无尽之刃',
            'plaintext': '大幅提升暴击伤害',
            'description': '+70攻击力 +20%暴击几率\n被动: 暴击造成225%伤害',
            'gold_total': 3400,
            'gold_base': 340,
            'gold_sell': 1360,
            'tags': '攻击,暴击',
            'stats': '{"attack_damage": 70, "crit_chance": 0.2}',
            'depth': 3,
            'category': '传说装备',
            'version': '13.24'
        },
        {
            'item_id': 3153,
            'name': '破败王者之刃',
            'plaintext': '对高生命值目标造成额外伤害',
            'description': '+40攻击力 +30%攻击速度 +8%生命偷取\n被动: 普攻造成目标当前生命值8%的额外物理伤害',
            'gold_total': 3300,
            'gold_base': 330,
            'gold_sell': 1320,
            'tags': '攻击,攻速,生命偷取',
            'stats': '{"attack_damage": 40, "attack_speed": 0.3, "life_steal": 0.08}',
            'depth': 3,
            'category': '传说装备',
            'version': '13.24'
        },
        {
            'item_id': 3020,
            'name': '女神之泪',
            'plaintext': '随时间获得额外法力值',
            'description': '+250法力值 +5技能急速\n被动: 法力积攒',
            'gold_total': 400,
            'gold_base': 400,
            'gold_sell': 160,
            'tags': '法力,冷却缩减',
            'stats': '{"mana": 250, "ability_haste": 5}',
            'depth': 1,
            'category': '基础装备',
            'version': '13.24'
        }
    ]
    
    for item in sample_items:
        cursor.execute('''
        INSERT OR REPLACE INTO items 
        (item_id, name, plaintext, description, gold_total, gold_base, gold_sell, tags, stats, depth, category, version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['item_id'], item['name'], item['plaintext'], item['description'],
            item['gold_total'], item['gold_base'], item['gold_sell'], item['tags'],
            item['stats'], item['depth'], item['category'], item['version']
        ))
    
    conn.commit()
    print(f"✅ 已插入 {len(sample_items)} 件示例装备")
    
    # 显示统计信息
    cursor.execute('SELECT COUNT(*) FROM items')
    count = cursor.fetchone()[0]
    cursor.execute('SELECT MIN(gold_total), MAX(gold_total), AVG(gold_total) FROM items')
    min_price, max_price, avg_price = cursor.fetchone()
    
    print(f"\n📊 数据库统计:")
    print(f"   总装备数: {count}")
    print(f"   价格范围: {min_price} - {max_price} 金币")
    print(f"   平均价格: {int(avg_price)} 金币")
    
    cursor.execute('SELECT name, gold_total FROM items ORDER BY gold_total DESC LIMIT 3')
    expensive = cursor.fetchall()
    print(f"   最贵装备:")
    for name, price in expensive:
        print(f"     - {name}: {price} 金币")

def main():
    """主函数"""
    print("=" * 60)
    print("🎮 英雄联盟装备数据导入工具")
    print("=" * 60)
    
    try:
        # 初始化数据库
        conn = init_database()
        
        # 插入示例数据
        insert_sample_data(conn)
        
        # 关闭连接
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ 数据导入完成!")
        print(f"📁 数据库文件: lol_items.db")
        print(f"⏰ 完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 检查文件大小
        db_size = os.path.getsize('lol_items.db') // 1024
        print(f"💾 数据库大小: {db_size} KB")
        
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
