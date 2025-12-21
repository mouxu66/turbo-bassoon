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
        
        cursor.execute("SELECT COUNT(*) FROM items")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total) FROM items WHERE gold_total > 0")
        min_price, max_price = cursor.fetchone()
        
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
            }
            h1 { 
                color: gold; 
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .card {
                background: rgba(30, 35, 40, 0.9);
                border-radius: 15px;
                padding: 30px;
                margin: 30px auto;
                max-width: 600px;
                border: 2px solid #c8aa6e;
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
            }
            .stats {
                display: inline-block;
                background: rgba(255,255,255,0.05);
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
            }
            .stat-num {
                font-size: 2em;
                color: gold;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🎮 英雄联盟装备数据库</h1>
        
        <div class="card">
            <h2>✅ 网站运行正常！</h2>
    '''
    
    if stats:
        html += f'''
            <div class="stats">
                <div class="stat-num">{stats['total']}</div>
                <div>件装备</div>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="/api/items" class="btn">📊 查看API数据</a>
                <a href="/items" class="btn">🛡️ 装备列表</a>
            </div>
            
            <h3>最贵装备：</h3>
        '''
        
        for name, price in stats['expensive']:
            html += f'<p>• {name}: {price} 金币</p>'
    else:
        html += '''
            <p>数据库连接错误</p>
            <a href="/api/items" class="btn">测试API</a>
        '''
    
    html += f'''
            <p style="margin-top: 30px; color: #a09b8c;">
                网址: https://mouxu.pythonanywhere.com<br>
                时间: {time.strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/api/items')
def api_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total FROM items")
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items')
def items():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total FROM items")
        items_data = cursor.fetchall()
        conn.close()
        
        html = '''
        <html>
        <head><title>装备列表</title></head>
        <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
            <h1>装备列表</h1>
            <a href="/">← 返回</a>
            <hr>
        '''
        
        for item_id, name, price in items_data:
            html += f'''
            <div style="background:rgba(255,255,255,0.05);margin:10px;padding:10px;">
                <strong>{name}</strong> - {price} 金币
                <a href="/item/{item_id}" style="color:gold;">详情</a>
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
        cursor.execute("SELECT name, gold_total, description FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return "装备不存在", 404
        
        name, price, desc = item
        
        return f'''
        <html>
        <head><title>{name}</title></head>
        <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
            <h1>{name}</h1>
            <p>💰 {price} 金币</p>
            {f'<p>{desc}</p>' if desc else ''}
            <a href="/items">← 返回列表</a>
        </body>
        </html>
        '''
    except Exception as e:
        return f"错误: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
