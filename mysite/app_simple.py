from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# 简化版本，避免API调用错误
@app.route('/')
def home():
    """简单的首页"""
    champions = [
        {'name': '亚托克斯', 'title': '暗裔剑魔', 'win_rate': 52.3, 'pick_rate': 8.1, 'tier': 'S', 'tags': ['战士', '坦克']},
        {'name': '阿狸', 'title': '九尾妖狐', 'win_rate': 50.8, 'pick_rate': 6.5, 'tier': 'A', 'tags': ['法师', '刺客']},
        {'name': '亚索', 'title': '疾风剑豪', 'win_rate': 49.5, 'pick_rate': 12.3, 'tier': 'B', 'tags': ['战士', '刺客']},
    ]
    return render_template('index.html', 
                         champions=champions,
                         version='14.1.1',
                         now=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route('/champion/<name>')
def champion_detail(name):
    """英雄详情页"""
    champion = {
        'name': name,
        'title': '英雄',
        'lore': f'这是{name}的背景故事...',
        'tags': ['战士', '坦克']
    }
    return render_template('champion.html',
                         champion=champion,
                         now=datetime.now().year)

@app.route('/api/health')
def health_check():
    """API健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '网站运行正常',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
