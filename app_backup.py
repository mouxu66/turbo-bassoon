from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import json
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

def get_db_stats():
    """获取数据库统计"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute("SELECT COUNT(*) FROM items")
        total = cursor.fetchone()[0]
        
        # 价格统计
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total) FROM items WHERE gold_total > 0")
        min_price, max_price = cursor.fetchone()
        
        # 最贵装备
        cursor.execute("SELECT name, gold_total FROM items WHERE gold_total > 0 ORDER BY gold_total DESC LIMIT 3")
        expensive = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'min_price': min_price or 0,
            'max_price': max_price or 0,
            'expensive': expensive
        }
    except Exception as e:
        print(f"数据库错误: {e}")
        return None

# 简单首页
@app.route('/')
def home():
    stats = get_db_stats()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 LoL装备数据库</title>
        <style>
            body { 
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e; 
                font-family: Arial, sans-serif;
                padding: 50px; 
                text-align: center;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 30px;
            }
            h1 { 
                color: gold; 
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .status-card {
                background: rgba(30, 35, 40, 0.9);
                border-radius: 15px;
                padding: 30px;
                margin: 30px 0;
                border: 2px solid #c8aa6e;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-item {
                background: rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                color: gold;
                font-weight: bold;
                margin: 10px 0;
            }
            .btn { 
                display: inline-block;
                background: gold; 
                color: black; 
                padding: 12px 24px; 
                margin: 10px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: bold;
                font-size: 1.1em;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
            }
            .item-card {
                background: rgba(255,255,255,0.03);
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #ffd700;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 英雄联盟装备数据库</h1>
            
            <div class="status-card">
                <h2>✅ PythonAnywhere运行成功！</h2>
                <p>你的网站已部署并可公开访问</p>
            </div>
    '''
    
    if stats:
        html += f'''
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{stats['total']}</div>
                    <div>总装备数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats['min_price']}-{stats['max_price']}</div>
                    <div>价格范围</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(stats['expensive'])}</div>
                    <div>顶级装备</div>
                </div>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="/api/items" class="btn">📊 查看完整API数据</a>
                <a href="/items" class="btn">🛡️ 网页查看装备</a>
                <a href="/health" class="btn">❤️ 健康检查</a>
            </div>
            
            <h3>💰 最贵装备：</h3>
        '''
        
        for name, price in stats['expensive']:
            html += f'''
            <div class="item-card">
                <strong>{name}</strong> - {price} 金币
            </div>
            '''
    else:
        html += '''
            <div style="margin: 30px 0;">
                <a href="/api/items" class="btn">📊 测试API连接</a>
            </div>
        '''
    
    html += f'''
            <div style="margin-top: 40px; color: #a09b8c;">
                <p>🔗 网站地址: https://mouxu.pythonanywhere.com</p>
                <p>⏰ 时间: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

# API接口
@app.route('/api/items')
def api_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(items),
            'items': items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items')
def items_page():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total, category FROM items ORDER BY name")
        items = cursor.fetchall()
        conn.close()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备列表</title>
            <style>
                body { background: #0a1428; color: #c8aa6e; padding: 20px; }
                .item { 
                    background: rgba(255,255,255,0.05); 
                    margin: 10px; 
                    padding: 15px; 
                    border-radius: 8px;
                    border-left: 4px solid #c8aa6e;
                }
                a { color: gold; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''
        
        for item_id, name, price, category in items:
            html += f'''
            <div class="item">
                <strong>{name}</strong>
                <div>💰 {price if price else 0} 金币</div>
                {f'<div>📁 {category}</div>' if category else ''}
                <a href="/item/{item_id}">查看详情</a>
            </div>
            '''
        
        html += f'''
            <hr>
            <p>共 {len(items)} 件装备</p>
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
        cursor.execute("SELECT name, gold_total, description FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return "装备不存在", 404
        
        name, price, description = item
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>{name}</title></head>
        <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
            <h1>{name}</h1>
            <p>💰 价格: {price if price else 0} 金币</p>
            {f'<p>📝 描述: {description}</p>' if description else ''}
            <a href="/items">← 返回列表</a>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': {
            'path': DB_PATH,
            'exists': os.path.exists(DB_PATH),
            'size_kb': os.path.getsize(DB_PATH)//1024 if os.path.exists(DB_PATH) else 0
        },
        'url': 'https://mouxu.pythonanywhere.com',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)
EOFcd /home/mouxu

# 创建完整的app.py文件
cat > app.py << 'EOF'
from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import json
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

def get_db_stats():
    """获取数据库统计"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute("SELECT COUNT(*) FROM items")
        total = cursor.fetchone()[0]
        
        # 价格统计
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total) FROM items WHERE gold_total > 0")
        min_price, max_price = cursor.fetchone()
        
        # 最贵装备
        cursor.execute("SELECT name, gold_total FROM items WHERE gold_total > 0 ORDER BY gold_total DESC LIMIT 3")
        expensive = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'min_price': min_price or 0,
            'max_price': max_price or 0,
            'expensive': expensive
        }
    except Exception as e:
        print(f"数据库错误: {e}")
        return None

# 简单首页
@app.route('/')
def home():
    stats = get_db_stats()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 LoL装备数据库</title>
        <style>
            body { 
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e; 
                font-family: Arial, sans-serif;
                padding: 50px; 
                text-align: center;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 30px;
            }
            h1 { 
                color: gold; 
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .status-card {
                background: rgba(30, 35, 40, 0.9);
                border-radius: 15px;
                padding: 30px;
                margin: 30px 0;
                border: 2px solid #c8aa6e;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-item {
                background: rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                color: gold;
                font-weight: bold;
                margin: 10px 0;
            }
            .btn { 
                display: inline-block;
                background: gold; 
                color: black; 
                padding: 12px 24px; 
                margin: 10px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: bold;
                font-size: 1.1em;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
            }
            .item-card {
                background: rgba(255,255,255,0.03);
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #ffd700;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 英雄联盟装备数据库</h1>
            
            <div class="status-card">
                <h2>✅ PythonAnywhere运行成功！</h2>
                <p>你的网站已部署并可公开访问</p>
            </div>
    '''
    
    if stats:
        html += f'''
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{stats['total']}</div>
                    <div>总装备数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats['min_price']}-{stats['max_price']}</div>
                    <div>价格范围</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(stats['expensive'])}</div>
                    <div>顶级装备</div>
                </div>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="/api/items" class="btn">📊 查看完整API数据</a>
                <a href="/items" class="btn">🛡️ 网页查看装备</a>
                <a href="/health" class="btn">❤️ 健康检查</a>
            </div>
            
            <h3>💰 最贵装备：</h3>
        '''
        
        for name, price in stats['expensive']:
            html += f'''
            <div class="item-card">
                <strong>{name}</strong> - {price} 金币
            </div>
            '''
    else:
        html += '''
            <div style="margin: 30px 0;">
                <a href="/api/items" class="btn">📊 测试API连接</a>
            </div>
        '''
    
    html += f'''
            <div style="margin-top: 40px; color: #a09b8c;">
                <p>🔗 网站地址: https://mouxu.pythonanywhere.com</p>
                <p>⏰ 时间: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

# API接口
@app.route('/api/items')
def api_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(items),
            'items': items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items')
def items_page():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total, category FROM items ORDER BY name")
        items = cursor.fetchall()
        conn.close()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备列表</title>
            <style>
                body { background: #0a1428; color: #c8aa6e; padding: 20px; }
                .item { 
                    background: rgba(255,255,255,0.05); 
                    margin: 10px; 
                    padding: 15px; 
                    border-radius: 8px;
                    border-left: 4px solid #c8aa6e;
                }
                a { color: gold; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''
        
        for item_id, name, price, category in items:
            html += f'''
            <div class="item">
                <strong>{name}</strong>
                <div>💰 {price if price else 0} 金币</div>
                {f'<div>📁 {category}</div>' if category else ''}
                <a href="/item/{item_id}">查看详情</a>
            </div>
            '''
        
        html += f'''
            <hr>
            <p>共 {len(items)} 件装备</p>
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
        cursor.execute("SELECT name, gold_total, description FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return "装备不存在", 404
        
        name, price, description = item
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>{name}</title></head>
        <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
            <h1>{name}</h1>
            <p>💰 价格: {price if price else 0} 金币</p>
            {f'<p>📝 描述: {description}</p>' if description else ''}
            <a href="/items">← 返回列表</a>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': {
            'path': DB_PATH,
            'exists': os.path.exists(DB_PATH),
            'size_kb': os.path.getsize(DB_PATH)//1024 if os.path.exists(DB_PATH) else 0
        },
        'url': 'https://mouxu.pythonanywhere.com',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)
