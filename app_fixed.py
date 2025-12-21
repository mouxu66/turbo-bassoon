from flask import Flask, jsonify
import sqlite3
import os
import time

app = Flask(__name__)

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

def get_db_stats():
    """获取数据库统计信息"""
    if not os.path.exists(DB_PATH):
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        
        # 获取价格范围
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total) FROM items WHERE gold_total > 0")
        min_price, max_price = cursor.fetchone()
        
        # 获取分类数量
        cursor.execute("SELECT COUNT(DISTINCT category) FROM items WHERE category IS NOT NULL")
        categories = cursor.fetchone()[0]
        
        # 获取一些示例
        cursor.execute("SELECT name, gold_total FROM items ORDER BY gold_total DESC LIMIT 3")
        expensive = cursor.fetchall()
        
        conn.close()
        
        return {
            'count': count,
            'min_price': min_price or 0,
            'max_price': max_price or 0,
            'categories': categories,
            'expensive': expensive,
            'file_size': os.path.getsize(DB_PATH) // 1024 if os.path.exists(DB_PATH) else 0
        }
    except Exception as e:
        print(f"数据库错误: {e}")
        return None

@app.route('/')
def index():
    stats = get_db_stats()
    db_exists = os.path.exists(DB_PATH)
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>LoL装备数据库</title>
        <style>
            body {{
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 30px;
                background: rgba(30, 35, 40, 0.8);
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
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin: 10px 0;
            }}
            .ok {{ background: rgba(0, 255, 0, 0.2); color: #00ff00; }}
            .error {{ background: rgba(255, 0, 0, 0.2); color: #ff5555; }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 1px solid rgba(200, 170, 110, 0.3);
            }}
            .stat-number {{
                font-size: 2em;
                color: #ffd700;
                font-weight: bold;
                margin: 10px 0;
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
                transition: transform 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-2px);
            }}
            .example-item {{
                background: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #ffd700;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 英雄联盟装备数据库</h1>
                <p>PythonAnywhere 运行版</p>
                
                <div class="status {'ok' if db_exists else 'error'}">
                    📊 数据库: {'✅ 已加载' if db_exists else '❌ 不存在'}
                </div>
            </div>
    '''
    
    if stats:
        html += f'''
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats['count']}</div>
                    <div>总装备数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['categories']}</div>
                    <div>分类数量</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['file_size']} KB</div>
                    <div>数据库大小</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['min_price']}-{stats['max_price']}</div>
                    <div>价格范围</div>
                </div>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="/items" class="btn">🛡️ 查看装备列表</a>
                <a href="/api/stats" class="btn">📊 API数据</a>
                <a href="/import" class="btn">📥 导入更多</a>
            </div>
            
            <h3>💰 最贵装备:</h3>
        '''
        
        for name, price in stats['expensive']:
            html += f'''
            <div class="example-item">
                <strong>{name}</strong> - {price} 金币
            </div>
            '''
    else:
        html += '''
            <div style="text-align: center; padding: 40px;">
                <h3>📭 数据库为空</h3>
                <p>请先导入装备数据</p>
                <a href="/import" class="btn">📥 立即导入</a>
            </div>
        '''
    
    html += f'''
            <div style="margin-top: 40px; text-align: center; color: #a09b8c;">
                <p>服务器时间: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>数据库路径: {DB_PATH}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/items')
def items():
    if not os.path.exists(DB_PATH):
        return "数据库不存在", 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT item_id, name, gold_total, category FROM items ORDER BY name")
        items_data = cursor.fetchall()
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
                .item-name { color: #ffd700; font-size: 1.2em; }
                .item-cost { color: #48bb78; font-weight: bold; }
                .item-category { color: #a09b8c; font-size: 0.9em; }
                a { color: #667eea; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''
        
        for item_id, name, cost, category in items_data:
            html += f'''
            <div class="item-card">
                <div class="item-name">{name}</div>
                <div class="item-cost">💰 {cost if cost else 0} 金币</div>
                <div class="item-category">{category if category else '未分类'}</div>
                <a href="/item/{item_id}">查看详情</a>
            </div>
            '''
        
        html += f'''
            <hr>
            <p>共 {len(items_data)} 件装备</p>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return "装备不存在", 404
        
        # 获取列名
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(items)")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()
        
        # 构建详情页面
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{item[columns.index('name')]}</title>
            <style>
                body {{ background: #0a1428; color: #c8aa6e; padding: 20px; }}
                .detail-card {{ 
                    background: rgba(30, 35, 40, 0.8); 
                    padding: 25px; 
                    border-radius: 10px;
                    border: 2px solid #c8aa6e;
                }}
                h1 {{ color: #ffd700; }}
                .price {{ 
                    font-size: 1.5em; 
                    color: gold; 
                    font-weight: bold;
                    margin: 15px 0;
                }}
                .property {{ 
                    margin: 10px 0; 
                    padding: 8px 12px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 5px;
                }}
                .prop-label {{ color: #a09b8c; font-weight: bold; }}
                a {{ color: #667eea; }}
            </style>
        </head>
        <body>
            <a href="/items">← 返回列表</a>
            <div class="detail-card">
                <h1>{item[columns.index('name')]}</h1>
                <div class="price">💰 {item[columns.index('gold_total')] if 'gold_total' in columns else 0} 金币</div>
        '''
        
        # 显示重要属性
        important_cols = ['plaintext', 'description', 'category', 'tags', 'version']
        for col in important_cols:
            if col in columns:
                idx = columns.index(col)
                value = item[idx]
                if value:
                    html += f'''
                    <div class="property">
                        <div class="prop-label">{col}:</div>
                        <div>{value}</div>
                    </div>
                    '''
        
        html += '''
            </div>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/import')
def import_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>导入数据</title></head>
    <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
        <h1>📥 导入装备数据</h1>
        <p>已自动导入示例数据。</p>
        <p>如需导入真实数据，需要：</p>
        <ol>
            <li>申请 Riot Games API Key</li>
            <li>修改 import_new.py 脚本</li>
            <li>运行 python import_new.py</li>
        </ol>
        <a href="/">← 返回首页</a>
    </body>
    </html>
    '''

@app.route('/api/stats')
def api_stats():
    stats = get_db_stats()
    return jsonify({
        'status': 'ok',
        'database': {
            'exists': os.path.exists(DB_PATH),
            'path': DB_PATH,
            'stats': stats
        },
        'server_time': time.strftime("%Y-%m-%d %H:%M:%S")
    })

# Flask应用入口
if __name__ == '__main__':
    app.run(debug=True)
