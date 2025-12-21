from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import json
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

# 简单首页
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 LoL装备数据库</title>
        <style>
            body { background: #0a1428; color: #c8aa6e; padding: 50px; text-align: center; }
            h1 { color: gold; }
            .btn { background: gold; color: black; padding: 12px 24px; margin: 10px; 
                   text-decoration: none; border-radius: 8px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>✅ 英雄联盟装备数据库</h1>
        <p>PythonAnywhere运行成功！</p>
        <a href="/api/items" class="btn">查看装备数据</a>
    </body>
    </html>
    '''

# 简单API
@app.route('/api/items')
def api_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total FROM items LIMIT 10")
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
