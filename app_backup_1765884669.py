from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

def get_db_info():
    """获取数据库信息 - 自适应列名"""
    if not os.path.exists(DB_PATH):
        return {'exists': False, 'error': '数据库文件不存在'}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        if not cursor.fetchone():
            conn.close()
            return {'exists': True, 'error': 'items表不存在'}
        
        # 2. 获取列信息
        cursor.execute("PRAGMA table_info(items)")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]
        
        # 3. 查找价格列（可能叫cost、price、gold_total等）
        price_columns = ['cost', 'price', 'gold', 'gold_total', 'gold_cost']
        price_column = None
        for col in price_columns:
            if col in columns:
                price_column = col
                break
        
        # 4. 获取数据统计
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0] or 0
        
        # 5. 获取示例数据
        examples = {}
        if count > 0 and price_column:
            cursor.execute(f"SELECT name, {price_column} FROM items WHERE {price_column} IS NOT NULL ORDER BY {price_column} DESC LIMIT 3")
            examples['expensive'] = cursor.fetchall()
            
            cursor.execute(f"SELECT name, {price_column} FROM items WHERE {price_column} IS NOT NULL AND {price_column} > 0 ORDER BY {price_column} ASC LIMIT 3")
            examples['cheap'] = cursor.fetchall()
        
        conn.close()
        
        return {
            'exists': True,
            'table_exists': True,
            'columns': columns,
            'price_column': price_column,
            'count': count,
            'examples': examples,
            'file_size': os.path.getsize(DB_PATH) // 1024
        }
        
    except Exception as e:
        return {'exists': True, 'error': f'数据库错误: {str(e)}'}

@app.route('/')
def home():
    """首页 - 显示数据库真实状态"""
    db_info = get_db_info()
    
    # 构建状态信息
    if not db_info.get('exists'):
        status = "❌ 数据库文件不存在"
        color = "#ff5555"
    elif db_info.get('error'):
        status = f"⚠️ {db_info['error']}"
        color = "#ffaa00"
    else:
        status = f"✅ 数据库正常 ({db_info['count']} 件装备)"
        color = "#00ff00"
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 LoL装备数据库 - PythonAnywhere</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 30px;
                background: rgba(30, 35, 40, 0.9);
                border-radius: 15px;
                border: 2px solid #c8aa6e;
                margin-bottom: 30px;
            }}
            h1 {{
                color: #ffd700;
                font-size: 2.5em;
                margin: 0 0 10px 0;
            }}
            .status {{
                display: inline-block;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin: 15px 0;
                background: rgba(255,255,255,0.1);
            }}
            .info-box {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #0a74da;
            }}
            .btn {{
                display: inline-block;
                background: gold;
                color: black;
                padding: 12px 24px;
                margin: 10px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 1.1em;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
            }}
            .column-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin: 10px 0;
            }}
            .column-tag {{
                background: rgba(100, 126, 234, 0.2);
                color: #a3bffa;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 英雄联盟装备数据库</h1>
                <p>PythonAnywhere - 数据库诊断版</p>
                
                <div class="status" style="border-color: {color}; color: {color};">
                    {status}
                </div>
            </div>
    '''
    
    # 显示数据库详细信息
    if db_info.get('exists') and not db_info.get('error'):
        html += f'''
            <div class="info-box">
                <h3>📊 数据库信息</h3>
                <p>📁 文件: {DB_PATH}</p>
                <p>📦 装备数量: {db_info['count']} 件</p>
                <p>💾 文件大小: {db_info['file_size']} KB</p>
                
                <h4>📋 表结构 (items表):</h4>
                <div class="column-list">
        '''
        
        for column in db_info['columns']:
            is_price = column == db_info['price_column']
            html += f'<span class="column-tag" style="border: 2px solid {"gold" if is_price else "transparent"}">{column}</span>'
        
        html += '''
                </div>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="/api/items" class="btn">📊 查看所有装备 (JSON)</a>
                <a href="/view-items" class="btn">👀 网页查看装备</a>
                <a href="/health" class="btn">❤️ 健康检查</a>
            </div>
        '''
        
        # 显示示例装备
        if db_info['count'] > 0 and db_info['price_column']:
            html += '''
            <div class="info-box">
                <h3>💰 装备示例:</h3>
            '''
            
            if db_info['examples'].get('expensive'):
                html += '<h4>最贵装备:</h4>'
                for name, price in db_info['examples']['expensive']:
                    html += f'<p>• {name}: {price} 金币</p>'
            
            html += '</div>'
    
    # 如果数据库有问题
    elif db_info.get('error'):
        html += f'''
            <div class="info-box" style="border-color: #ff5555;">
                <h3>⚠️ 数据库问题</h3>
                <p>错误: {db_info['error']}</p>
                <p>请检查数据库表结构是否匹配应用代码。</p>
                <p>数据库路径: {DB_PATH}</p>
                
                <div style="margin-top: 20px;">
                    <a href="/fix-db" class="btn" style="background: #48bb78;">🔧 修复数据库</a>
                    <a href="/create-db" class="btn" style="background: #667eea;">🆕 创建新数据库</a>
                </div>
            </div>
        '''
    
    # 关闭HTML
    html += f'''
            <div style="margin-top: 40px; text-align: center; color: #a09b8c;">
                <p>服务器时间: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>网站地址: https://mouxu.pythonanywhere.com</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/api/items')
def api_items():
    """自适应列名的API接口"""
    db_info = get_db_info()
    
    if not db_info.get('exists') or db_info.get('error'):
        return jsonify({'error': db_info.get('error', '数据库问题')}), 500
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 构建查询 - 使用实际的列名
        columns = db_info['columns']
        select_columns = ', '.join(columns)
        cursor.execute(f"SELECT {select_columns} FROM items")
        
        items = []
        for row in cursor.fetchall():
            item = {}
            for col in columns:
                item[col] = row[col]
            items.append(item)
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(items),
            'columns': columns,
            'items': items
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view-items')
def view_items():
    """网页查看装备"""
    db_info = get_db_info()
    
    if not db_info.get('exists') or db_info.get('error'):
        return f"数据库错误: {db_info.get('error', '未知错误')}", 500
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有装备
        cursor.execute("SELECT * FROM items")
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
                    margin: 15px; 
                    padding: 15px; 
                    border-radius: 10px;
                    border-left: 4px solid #c8aa6e;
                }
                .item-name { color: #ffd700; font-size: 1.2em; }
                a { color: gold; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''
        
        for item in items:
            # 第一列是ID，第二列通常是name
            name = item[1] if len(item) > 1 else "未知"
            html += f'''
            <div class="item-card">
                <div class="item-name">{name}</div>
                <div>ID: {item[0]} | 共 {len(item)} 个属性</div>
            </div>
            '''
        
        html += f'''
            <hr>
            <p>共 {len(items)} 件装备</p>
            <p>数据库列: {', '.join(db_info['columns'])}</p>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/health')
def health():
    """健康检查"""
    db_info = get_db_info()
    return jsonify({
        'app': 'lol-items-database',
        'status': 'running',
        'database': db_info,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': 'https://mouxu.pythonanywhere.com'
    })

@app.route('/fix-db')
def fix_database():
    """修复数据库（重新创建表）"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 备份旧表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE items RENAME TO items_old")
            print("已备份旧表")
        
        # 创建标准表结构
        cursor.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            price INTEGER,
            description TEXT,
            effect TEXT,
            image TEXT DEFAULT ''
        )
        ''')
        
        # 如果有旧数据，尝试迁移
        try:
            cursor.execute("SELECT name, type, price, description, effect FROM items_old")
            old_items = cursor.fetchall()
            
            for item in old_items:
                cursor.execute(
                    "INSERT INTO items (name, type, price, description, effect) VALUES (?, ?, ?, ?, ?)",
                    item
                )
            print(f"迁移了 {len(old_items)} 件装备")
        except:
            print("无法迁移旧数据")
        
        # 如果数据为空，添加示例
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_items = [
                ('无尽之刃', '攻击', 3400, '传说之刃，能造成毁灭性的暴击伤害', '+70攻击力 +20%暴击率'),
                ('灭世者的死亡之帽', '法术', 3600, '一顶强大的帽子，能极大提升法术强度', '+120法术强度'),
                ('日炎圣盾', '防御', 2800, '燃烧的护盾，能对附近敌人造成伤害', '+450生命值 +50护甲')
            ]
            cursor.executemany(
                "INSERT INTO items (name, type, price, description, effect) VALUES (?, ?, ?, ?, ?)",
                sample_items
            )
            print(f"添加了 {len(sample_items)} 件示例装备")
        
        conn.commit()
        conn.close()
        
        return '''
        <html>
        <body style="background:#0a1428;color:#c8aa6e;padding:50px;text-align:center;">
            <h1>✅ 数据库修复完成！</h1>
            <p>表结构已标准化，数据已迁移。</p>
            <a href="/" style="color:gold;">返回首页</a>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f"修复失败: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
