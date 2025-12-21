"""
轻量版应用 - 专门用于PythonAnywhere免费账户
"""
from flask import Flask, render_template, jsonify
import sqlite3
import os
import logging

# 禁用详细日志
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mouxu-light-2024'

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'lol_data.db')

def get_db():
    """获取数据库连接（简化版）"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        return conn
    except:
        return None

@app.route('/')
def home():
    """首页 - 极简版"""
    item_count = 0
    match_count = 0
    
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM items")
            item_count = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM matches")
            match_count = cursor.fetchone()[0] or 0
            conn.close()
        except:
            pass
    
    return render_template('index.html',
                         item_count=item_count,
                         match_count=match_count)

@app.route('/items')
def items():
    """装备页面 - 简化版"""
    conn = get_db()
    items = []
    
    if conn:
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name, gold_total, ad, ap FROM items LIMIT 20")
            items = cursor.fetchall()
            conn.close()
        except:
            pass
    
    return render_template('items.html', items=items)

@app.route('/match_analysis')
def match_analysis():
    """分析页面"""
    return render_template('match_analysis.html')

@app.route('/upload')
def upload():
    """上传页面"""
    return render_template('upload.html')

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # 确保目录存在
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'templates'), exist_ok=True)
    
    print("轻量版应用启动 - CPU优化")
    app.run(debug=False)
