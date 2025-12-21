# final_app_pa_fixed.py - PythonAnywhere专用修复版
from flask import Flask, render_template_string, jsonify
import sqlite3
import os
import time

app = Flask(__name__)

# 获取绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'lol_items.db')

def check_database():
    """检查数据库状态"""
    if not os.path.exists(DB_PATH):
        return False, "数据库文件不存在", 0, {}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        if not cursor.fetchone():
            conn.close()
            return True, "数据库存在但items表不存在", 0, {}
        
        # 获取数量
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0] or 0
        
        # 获取几个示例
        cursor.execute("SELECT name, cost FROM items WHERE cost IS NOT NULL ORDER BY cost DESC LIMIT 3")
        expensive = cursor.fetchall()
        cursor.execute("SELECT name, cost FROM items WHERE cost IS NOT NULL AND cost > 0 ORDER BY cost ASC LIMIT 3")
        cheap = cursor.fetchall()
        
        conn.close()
        
        examples = {
            'most_expensive': expensive,
            'cheapest': cheap,
            'total': count
        }
        
        return True, "数据库正常", count, examples
        
    except Exception as e:
        return False, f"数据库错误: {str(e)}", 0, {}

# ========== 路由定义 ==========

@app.route('/')
def index():
    """首页"""
    db_exists = os.path.exists(DB_PATH)
    
    if db_exists:
        db_ok, db_msg, db_count, examples = check_database()
    else:
        db_ok, db_msg, db_count, examples = False, "数据库不存在", 0, {}
    
    # 构建HTML内容
    html_content = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>英雄联盟装备数据库</title>
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
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding: 30px;
                background: rgba(30, 35, 40, 0.8);
                border-radius: 15px;
                border: 2px solid #c8aa6e;
            }}
            h1 {{
                color: #ffd700;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .status {{
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin: 10px 0;
            }}
            .status-ok {{
                background: #00ff0040;
                color: #00ff00;
            }}
            .status-error {{
                background: #ff000040;
                color: #ff5555;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-item {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 1px solid rgba(200, 170, 110, 0.3);
            }}
            .stat-number {{
                font-size: 2.5em;
                color: #ffd700;
                font-weight: bold;
            }}
            .stat-label {{
                color: #a09b8c;
                margin-top: 10px;
            }}
            .btn-group {{
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 30px;
                flex-wrap: wrap;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
                transition: transform 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-2px);
            }}
            .btn-home {{
                background: gold;
                color: black;
            }}
            .btn-items {{
                background: #667eea;
                color: white;
            }}
            .btn-import {{
                background: #48bb78;
                color: white;
            }}
            .examples {{
                margin-top: 40px;
            }}
            .example-card {{
                background: rgba(255, 255, 255, 0.03);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #ffd700;
            }}
            .example-name {{
                font-weight: bold;
                color: #ffffff;
            }}
            .example-price {{
                color: #ffd700;
                font-size: 1.2em;
            }}
            .info-box {{
                background: rgba(0, 100, 255, 0.1);
                border-left: 4px solid #0a74da;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 英雄联盟装备数据库</h1>
                <p>完整功能修复版 - PythonAnywhere</p>
                
                <div class="status {'status-ok' if db_ok else 'status-error'}">
                    📊 数据库状态: {db_msg}
                </div>
            </div>
    '''
    
    if db_ok and db_count > 0:
        # 添加统计信息
        html_content += f'''
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{db_count}</div>
                    <div class="stat-label">总装备数量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{os.path.getsize(DB_PATH) // 1024}</div>
                    <div class="stat-label">数据库大小 (KB)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{(db_count // 10) * 10}+</div>
                    <div class="stat-label">属性类型</div>
                </div>
            </div>
            
            <div class="info-box">
                <strong>📅 系统信息:</strong><br>
                服务器状态: <span style="color: #00ff00;">运行中</span><br>
                当前时间: {time.strftime("%Y-%m-%d %H:%M:%S")}<br>
                文件路径: {DB_PATH}
            </div>
        '''
        
        # 添加示例装备
        if examples.get('most_expensive') or examples.get('cheapest'):
            html_content += '''
            <div class="examples">
                <h3>📦 装备示例</h3>
            '''
            
            if examples.get('most_expensive'):
                html_content += '<h4>最贵装备:</h4>'
                for name, cost in examples['most_expensive']:
                    html_content += f'''
                    <div class="example-card">
                        <div class="example-name">{name}</div>
                        <div class="example-price">{cost if cost else 0} 金币</div>
                    </div>
                    '''
            
            if examples.get('cheapest'):
                html_content += '<h4>最便宜装备:</h4>'
                for name, cost in examples['cheapest']:
                    html_content += f'''
                    <div class="example-card">
                        <div class="example-name">{name}</div>
                        <div class="example-price">{cost if cost else 0} 金币</div>
                    </div>
                    '''
            
            html_content += '</div>'
    
    # 添加按钮组
    html_content += '''
            <div class="btn-group">
                <a href="/" class="btn btn-home">🏠 返回首页</a>
                <a href="/items" class="btn btn-items">🛡️ 查看装备</a>
                <a href="/import" class="btn btn-import">📥 导入数据</a>
            </div>
    '''
    
    # 如果没有数据
    if not db_ok or db_count == 0:
        html_content += f'''
            <div class="info-box">
                <h3>⚠️ 数据库为空或不存在</h3>
                <p>需要先导入装备数据才能使用完整功能。</p>
                <p>数据库路径: {DB_PATH}</p>
                <p>状态: {db_msg}</p>
            </div>
        '''
    
    # 关闭HTML
    html_content += '''
        </div>
    </body>
    </html>
    '''
    
    return html_content

@app.route('/items')
def items_list():
    """装备列表"""
    if not os.path.exists(DB_PATH):
        return "数据库不存在，请先导入数据", 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, cost, description FROM items ORDER BY name")
        items = cursor.fetchall()
        conn.close()
        
        if not items:
            return "数据库中没有装备数据", 404
        
        # 构建HTML
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备列表</title>
            <style>
                body { background: #0a1428; color: #c8aa6e; padding: 20px; }
                .item { background: rgba(255,255,255,0.05); margin: 10px; padding: 15px; border-radius: 8px; }
                .item-name { color: #ffd700; font-size: 1.2em; }
                .item-cost { color: #48bb78; }
                a { color: #667eea; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🛡️ 装备列表 (共 {} 件)</h1>
            <a href="/">← 返回首页</a>
            <hr>
        '''.format(len(items))
        
        for item in items:
            item_id, name, cost, description = item
            html += f'''
            <div class="item">
                <div class="item-name">{name}</div>
                <div class="item-cost">💰 {cost if cost else 0} 金币</div>
                <div class="item-desc">{description[:100] if description else "无描述"}...</div>
                <a href="/item/{item_id}">查看详情</a>
            </div>
            '''
        
        html += '''
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"数据库错误: {str(e)}", 500

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    """装备详情"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
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
        
        # 构建HTML
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{item[columns.index('name')] if 'name' in columns else '未知装备'}</title>
            <style>
                body {{ background: #0a1428; color: #c8aa6e; padding: 20px; }}
                .item-detail {{ max-width: 800px; margin: 0 auto; }}
                .item-header {{ background: rgba(200, 170, 110, 0.1); padding: 20px; border-radius: 10px; }}
                h1 {{ color: #ffd700; }}
                .property {{ margin: 10px 0; }}
                .prop-name {{ color: #a09b8c; }}
                .prop-value {{ color: white; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="item-detail">
                <a href="/items">← 返回列表</a>
                <div class="item-header">
                    <h1>{item[columns.index('name')] if 'name' in columns else '未知装备'}</h1>
                    <div style="color: #48bb78; font-size: 1.5em;">
                        💰 {item[columns.index('cost')] if 'cost' in columns else 0} 金币
                    </div>
                </div>
        '''
        
        # 显示所有属性
        for i, col_name in enumerate(columns):
            if i < len(item) and item[i] and col_name not in ['id', 'name', 'cost']:
                value = item[i]
                if value:
                    html += f'''
                    <div class="property">
                        <div class="prop-name">{col_name}:</div>
                        <div class="prop-value">{str(value)[:200]}{'...' if len(str(value)) > 200 else ''}</div>
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
def import_data():
    """数据导入页面"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>导入数据</title>
        <style>
            body { background: #0a1428; color: #c8aa6e; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; }
            a { color: #667eea; }
            .btn { 
                display: inline-block; 
                background: #48bb78; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 5px; 
                text-decoration: none;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📥 导入装备数据</h1>
            <p>需要使用 import_now.py 脚本导入数据：</p>
            <pre style="background: #1a1a1a; padding: 15px; border-radius: 5px;">
$ python import_now.py
            </pre>
            <p>或者直接运行：</p>
            <a href="/admin/import" class="btn">运行导入脚本</a>
            <br><br>
            <a href="/">← 返回首页</a>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/import')
def admin_import():
    """运行导入脚本"""
    try:
        # 尝试运行导入脚本
        import subprocess
        result = subprocess.run(['python', 'import_now.py'], 
                               capture_output=True, text=True, cwd=BASE_DIR)
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>导入结果</title></head>
        <body style="background:#0a1428;color:#c8aa6e;padding:20px;">
            <h1>导入结果</h1>
            <pre style="background:#1a1a1a;padding:15px;border-radius:5px;">
{result.stdout}
{result.stderr}
            </pre>
            <a href="/">返回首页</a>
        </body>
        </html>
        '''
    except Exception as e:
        return f"导入失败: {str(e)}", 500

@app.route('/api/status')
def api_status():
    """API状态检查"""
    db_ok, db_msg, db_count, examples = check_database()
    return jsonify({
        'status': 'ok',
        'database': {
            'exists': os.path.exists(DB_PATH),
            'ok': db_ok,
            'message': db_msg,
            'item_count': db_count
        },
        'server_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        'base_dir': BASE_DIR
    })

# 不再运行 app.run()，因为PythonAnywhere使用WSGI