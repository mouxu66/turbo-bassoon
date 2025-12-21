from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import csv
import json
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

# ========== 数据库初始化 ==========
def init_database():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建扩展的表结构
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        name TEXT NOT NULL,
        gold_total INTEGER DEFAULT 0,
        gold_sell INTEGER DEFAULT 0,
        ad REAL DEFAULT 0,          -- 攻击力
        as_ REAL DEFAULT 0,         -- 攻速
        crit REAL DEFAULT 0,        -- 暴击率
        ls REAL DEFAULT 0,          -- 生命偷取
        apen REAL DEFAULT 0,        -- 护甲穿透
        ap REAL DEFAULT 0,          -- 法术强度
        ah REAL DEFAULT 0,          -- 技能急速
        mana REAL DEFAULT 0,        -- 法力值
        mp5 REAL DEFAULT 0,         -- 法力回复
        hsp REAL DEFAULT 0,         -- 治疗和护盾强度
        ovamp REAL DEFAULT 0,       -- 全能吸血
        mpen REAL DEFAULT 0,        -- 法术穿透
        health REAL DEFAULT 0,      -- 生命值
        armor REAL DEFAULT 0,       -- 护甲
        mr REAL DEFAULT 0,          -- 魔法抗性
        hp5 REAL DEFAULT 0,         -- 生命回复
        ms REAL DEFAULT 0,          -- 移动速度
        maps TEXT DEFAULT 'All',    -- 可用地图
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        UNIQUE(item_id, name)
    )
    ''')
    
    conn.commit()
    conn.close()

# ========== 导入功能 ==========
def import_itemtbl():
    """导入ItemTbl.csv (636件基础装备)"""
    imported = 0
    updated = 0
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open('ItemTbl.csv', 'r', encoding='utf-8') as f:
            # 跳过可能的BOM
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            
            # 解析CSV
            reader = csv.reader(content.strip().splitlines())
            next(reader)  # 跳过标题行
            
            for row in reader:
                if len(row) >= 2:
                    item_id = int(row[0]) if row[0].isdigit() else 0
                    name = row[1].strip()
                    
                    if item_id and name:
                        cursor.execute('''
                            INSERT OR REPLACE INTO items (item_id, name)
                            VALUES (?, ?)
                        ''', (item_id, name))
                        
                        if cursor.rowcount == 1:
                            imported += 1
                        else:
                            updated += 1
        
        conn.commit()
        conn.close()
        return {'success': True, 'imported': imported, 'updated': updated, 'total': imported + updated}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def import_lol_stats():
    """导入LOL_items_stats.csv (195件详细装备数据)"""
    imported = 0
    updated = 0
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open('LOL_items_stats.csv', 'r', encoding='utf-8') as f:
            # 读取并清理数据
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            
            # 分号分隔的CSV
            reader = csv.reader(content.strip().splitlines(), delimiter=';')
            headers = next(reader)
            
            for row in reader:
                if len(row) >= 1:
                    name = row[0].strip()
                    if not name:
                        continue
                    
                    # 解析数值
                    cost = int(row[1]) if len(row) > 1 and row[1] and row[1].isdigit() else 0
                    sell = int(row[2]) if len(row) > 2 and row[2] and row[2].isdigit() else 0
                    
                    # 解析属性
                    ad = float(row[3]) if len(row) > 3 and row[3] else 0
                    as_ = float(row[4]) if len(row) > 4 and row[4] else 0
                    crit = float(row[5]) if len(row) > 5 and row[5] else 0
                    ls = float(row[6]) if len(row) > 6 and row[6] else 0
                    apen = float(row[7]) if len(row) > 7 and row[7] else 0
                    ap = float(row[8]) if len(row) > 8 and row[8] else 0
                    ah = float(row[9]) if len(row) > 9 and row[9] else 0
                    mana = float(row[10]) if len(row) > 10 and row[10] else 0
                    mp5 = float(row[11]) if len(row) > 11 and row[11] else 0
                    hsp = float(row[12]) if len(row) > 12 and row[12] else 0
                    ovamp = float(row[13]) if len(row) > 13 and row[13] else 0
                    mpen = float(row[14]) if len(row) > 14 and row[14] else 0
                    health = float(row[15]) if len(row) > 15 and row[15] else 0
                    armor = float(row[16]) if len(row) > 16 and row[16] else 0
                    mr = float(row[17]) if len(row) > 17 and row[17] else 0
                    hp5 = float(row[18]) if len(row) > 18 and row[18] else 0
                    ms = float(row[19]) if len(row) > 19 and row[19] else 0
                    maps = row[20] if len(row) > 20 else 'All'
                    
                    # 更新或插入
                    cursor.execute('''
                        INSERT OR REPLACE INTO items (
                            name, gold_total, gold_sell, ad, as_, crit, ls, apen, 
                            ap, ah, mana, mp5, hsp, ovamp, mpen, health, armor, 
                            mr, hp5, ms, maps
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        name, cost, sell, ad, as_, crit, ls, apen, ap, ah, mana, 
                        mp5, hsp, ovamp, mpen, health, armor, mr, hp5, ms, maps
                    ))
                    
                    if cursor.rowcount == 1:
                        imported += 1
                    else:
                        updated += 1
        
        conn.commit()
        conn.close()
        return {'success': True, 'imported': imported, 'updated': updated, 'total': imported + updated}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_database_stats():
    """获取数据库统计信息"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM items")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM items WHERE gold_total > 0")
        with_price = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total), AVG(gold_total) FROM items WHERE gold_total > 0")
        price_stats = cursor.fetchone()
        
        # 属性统计
        stats = {
            'total': total,
            'with_price': with_price,
            'min_price': price_stats[0] or 0,
            'max_price': price_stats[1] or 0,
            'avg_price': int(price_stats[2]) if price_stats[2] else 0,
            'attributes': {}
        }
        
        # 检查哪些属性有数据
        attributes = ['ad', 'ap', 'health', 'armor', 'mr', 'as_', 'crit']
        for attr in attributes:
            cursor.execute(f"SELECT COUNT(*) FROM items WHERE {attr} > 0")
            count = cursor.fetchone()[0]
            if count > 0:
                stats['attributes'][attr] = count
        
        conn.close()
        return stats
        
    except Exception as e:
        return {'error': str(e)}

# ========== 初始化数据库 ==========
init_database()

# ========== 路由定义 ==========
@app.route('/')
def home():
    stats = get_database_stats()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 LoL装备数据库 - 完整版</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 40px 30px;
                background: linear-gradient(135deg, rgba(30, 35, 40, 0.95), rgba(20, 25, 30, 0.95));
                border-radius: 20px;
                border: 3px solid #c8aa6e;
                margin-bottom: 30px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            }}
            h1 {{
                color: #ffd700;
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
                background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin: 40px 0;
            }}
            .stat-card {{
                background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                border: 1px solid rgba(200, 170, 110, 0.2);
                transition: all 0.3s ease;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
                border-color: #c8aa6e;
            }}
            .stat-number {{
                font-size: 2.5em;
                color: #ffd700;
                font-weight: bold;
                margin: 10px 0;
            }}
            .btn-group {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 40px 0;
                flex-wrap: wrap;
            }}
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: linear-gradient(135deg, gold, #ffcc00);
                color: black;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 1.2em;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
            }}
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
            }}
            .btn-import {{
                background: linear-gradient(135deg, #48bb78, #38a169);
                color: white;
            }}
            .btn-import:hover {{
                background: linear-gradient(135deg, #38a169, #48bb78);
            }}
            .import-section {{
                background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(20, 25, 30, 0.8));
                border-radius: 20px;
                padding: 40px;
                margin: 50px 0;
                border: 2px solid rgba(200, 170, 110, 0.3);
            }}
            .file-card {{
                background: rgba(255,255,255,0.03);
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
                border-left: 5px solid #0a74da;
            }}
            .attr-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            .attr-item {{
                background: rgba(72, 187, 120, 0.1);
                padding: 12px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid rgba(72, 187, 120, 0.2);
            }}
            .attr-name {{
                color: #a09b8c;
                font-size: 0.9em;
                margin-bottom: 5px;
            }}
            .attr-value {{
                color: #48bb78;
                font-weight: bold;
            }}
            @media (max-width: 768px) {{
                .container {{ padding: 10px; }}
                h1 {{ font-size: 2em; }}
                .btn-group {{ flex-direction: column; align-items: center; }}
                .btn {{ width: 100%; max-width: 300px; justify-content: center; }}
            }}
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-dragon"></i> 英雄联盟装备数据库</h1>
                <p style="color: #a09b8c; font-size: 1.2em; margin-bottom: 20px;">
                    专业版 • 完整装备数据系统
                </p>
                <div style="background: rgba(0, 255, 0, 0.1); color: #00ff00; 
                          padding: 10px 25px; border-radius: 20px; display: inline-block;
                          border: 2px solid #00ff00; font-weight: bold;">
                    <i class="fas fa-database"></i> 数据库就绪 • 等待导入
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats.get('total', 0)}</div>
                    <div>当前装备数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('with_price', 0)}</div>
                    <div>有价格数据</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('min_price', 0)}-{stats.get('max_price', 0)}</div>
                    <div>价格范围 (金币)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('avg_price', 0)}</div>
                    <div>平均价格</div>
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/items" class="btn">
                    <i class="fas fa-list"></i> 查看所有装备
                </a>
                <a href="/api/items" class="btn">
                    <i class="fas fa-code"></i> API 数据接口
                </a>
                <a href="/search" class="btn">
                    <i class="fas fa-search"></i> 搜索装备
                </a>
            </div>
            
            <div class="import-section">
                <h2 style="color: #ffd700; text-align: center; margin-bottom: 30px;">
                    <i class="fas fa-database"></i> 数据导入中心
                </h2>
                
                <div class="file-card">
                    <h3><i class="fas fa-file-csv"></i> ItemTbl.csv</h3>
                    <p><strong>636件基础装备</strong> • 包含装备ID和名称</p>
                    <p>格式: ItemID, ItemName (例如: 1001, Boots)</p>
                    <div style="margin-top: 20px;">
                        <a href="/import/itemtbl" class="btn btn-import" 
                           onclick="return confirm('导入636件基础装备？')">
                            <i class="fas fa-upload"></i> 导入基础装备列表
                        </a>
                    </div>
                </div>
                
                <div class="file-card">
                    <h3><i class="fas fa-chart-bar"></i> LOL_items_stats.csv</h3>
                    <p><strong>195件详细装备数据</strong> • 包含完整属性信息</p>
                    <p>20个属性字段: 价格、攻击力、法术强度、生命值、护甲等</p>
                    
                    <div class="attr-grid">
                        <div class="attr-item">
                            <div class="attr-name">💰 价格</div>
                            <div class="attr-value">Cost, Sell</div>
                        </div>
                        <div class="attr-item">
                            <div class="attr-name">⚔️ 攻击</div>
                            <div class="attr-value">AD, AS, Crit</div>
                        </div>
                        <div class="attr-item">
                            <div class="attr-name">🔮 法术</div>
                            <div class="attr-value">AP, AH, Mana</div>
                        </div>
                        <div class="attr-item">
                            <div class="attr-name">🛡️ 防御</div>
                            <div class="attr-value">Health, Armor, MR</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 20px;">
                        <a href="/import/stats" class="btn btn-import" 
                           onclick="return confirm('导入195件详细装备数据？')">
                            <i class="fas fa-upload"></i> 导入详细属性数据
                        </a>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/import/all" class="btn" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;"
                       onclick="return confirm('导入全部831件装备数据？这可能需要几秒钟。')">
                        <i class="fas fa-bolt"></i> 一键导入所有数据
                    </a>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 50px; color: #a09b8c;">
                <p><i class="fas fa-info-circle"></i> 导入后，你的数据库将拥有完整的英雄联盟装备数据</p>
                <p><i class="fas fa-globe"></i> 网站地址: https://mouxu.pythonanywhere.com</p>
                <p><i class="fas fa-clock"></i> 当前时间: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </div>
        
        <script>
            // 简单的交互效果
            document.addEventListener('DOMContentLoaded', function() {{
                const cards = document.querySelectorAll('.stat-card, .file-card');
                cards.forEach(card => {{
                    card.addEventListener('mouseenter', function() {{
                        this.style.transform = 'translateY(-5px)';
                    }});
                    card.addEventListener('mouseleave', function() {{
                        this.style.transform = 'translateY(0)';
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    '''

@app.route('/import/itemtbl')
def import_itemtbl_route():
    """导入ItemTbl.csv"""
    result = import_itemtbl()
    
    if result['success']:
        return f'''
        <html>
        <body style="background:#0a1428;color:gold;padding:50px;text-align:center;">
            <h1>✅ 基础装备导入成功！</h1>
            <p>新增: {result['imported']} 件装备</p>
            <p>更新: {result['updated']} 件装备</p>
            <p>总计: {result['total']} 件装备</p>
            <a href="/" style="color:gold;font-size:1.2em;">返回首页查看</a>
        </body>
        </html>
        '''
    else:
        return f"导入失败: {result['error']}", 500

@app.route('/import/stats')
def import_stats_route():
    """导入LOL_items_stats.csv"""
    result = import_lol_stats()
    
    if result['success']:
        return f'''
        <html>
        <body style="background:#0a1428;color:gold;padding:50px;text-align:center;">
            <h1>✅ 详细属性导入成功！</h1>
            <p>新增: {result['imported']} 件装备</p>
            <p>更新: {result['updated']} 件装备</p>
            <p>总计: {result['total']} 件装备</p>
            <p>现在装备拥有完整的属性数据</p>
            <a href="/" style="color:gold;font-size:1.2em;">返回首页查看</a>
        </body>
        </html>
        '''
    else:
        return f"导入失败: {result['error']}", 500

@app.route('/import/all')
def import_all_route():
    """导入所有数据"""
    result1 = import_itemtbl()
    result2 = import_lol_stats()
    
    total_imported = result1.get('imported', 0) + result2.get('imported', 0)
    total_updated = result1.get('updated', 0) + result2.get('updated', 0)
    
    return f'''
    <html>
    <body style="background:#0a1428;color:gold;padding:50px;text-align:center;">
        <h1>✅ 全部数据导入完成！</h1>
        <p>基础装备: {result1.get('total', 0)} 件</p>
        <p>详细属性: {result2.get('total', 0)} 件</p>
        <p>总计新增: {total_imported} 件</p>
        <p>总计更新: {total_updated} 件</p>
        <p style="margin-top:30px;font-size:1.2em;">
            现在你的数据库拥有完整的英雄联盟装备数据！
        </p>
        <a href="/" style="color:gold;font-size:1.2em;">返回首页查看完整数据库</a>
    </body>
    </html>
    '''

@app.route('/items')
def items_page():
    """装备列表页面"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total FROM items ORDER BY name LIMIT 100")
        items = cursor.fetchall()
        conn.close()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备列表</title>
            <style>
                body { background: #0a1428; color: #c8aa6e; padding: 20px; }
                .item-card { 
                    background: rgba(255,255,255,0.05); 
                    margin: 10px; 
                    padding: 15px; 
                    border-radius: 8px;
                    border-left: 4px solid #c8aa6e;
                }
                .item-name { color: white; font-weight: bold; }
                .item-price { color: #48bb78; }
                a { color: gold; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''
        
        for item_id, name, price in items:
            html += f'''
            <div class="item-card">
                <div class="item-name">{name}</div>
                <div class="item-price">💰 {price if price else '?'} 金币</div>
                <a href="/item/{item_id}">查看详情</a>
            </div>
            '''
        
        html += '''
            <hr>
            <p>显示前 100 件装备</p>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/api/items')
def api_items():
    """API接口"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items LIMIT 50")
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(items),
            'items': items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search')
def search_page():
    """搜索页面"""
    return '''
    <html>
    <body style="background:#0a1428;color:#c8aa6e;padding:50px;text-align:center;">
        <h1>🔍 搜索功能</h1>
        <p>数据导入后启用搜索功能</p>
        <a href="/">← 返回首页</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
