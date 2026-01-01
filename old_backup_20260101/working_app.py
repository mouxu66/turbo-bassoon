from flask import Flask
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def home():
    # 简单测试页面
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>LOL装备库</title></head>
    <body style="background:#0f0f23;color:white;text-align:center;padding:50px">
        <h1 style="color:gold">🏆 LOL装备数据库</h1>
        <p>网站正在运行！</p>
        <a href="/items" style="color:gold">查看装备</a>
    </body>
    </html>
    '''

@app.route('/items')
def items():
    try:
        conn = sqlite3.connect('lol_items.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, cost FROM items LIMIT 10')
        items = cursor.fetchall()
        conn.close()
        
        html = '<h1>装备列表</h1>'
        for name, cost in items:
            html += f'<div>{name} - {cost}金币</div>'
        return html
    except Exception as e:
        return f'错误: {str(e)}'

if __name__ == '__main__':
    app.run(debug=False)
