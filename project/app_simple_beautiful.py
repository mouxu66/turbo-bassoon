from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# 美化数据
BEAUTIFUL_DATA = {
    "project": {
        "name": "英雄联盟数据分析平台",
        "description": "基于Riot API的专业数据分析系统",
        "version": "v2.0",
        "author": "学生项目",
        "course": "Web开发与数据分析课程"
    },
    "features": [
        {"icon": "📊", "title": "数据统计", "desc": "实时游戏数据分析"},
        {"icon": "🏆", "title": "英雄梯度", "desc": "版本强势英雄排行"},
        {"icon": "👤", "title": "玩家查询", "desc": "个人战绩与统计"},
        {"icon": "💻", "title": "API集成", "desc": "Riot官方API调用"},
        {"icon": "🔧", "title": "开源生态", "desc": "GitHub项目集成"},
        {"icon": "📈", "title": "可视化", "desc": "数据图表展示"}
    ],
    "stats": {
        "champions_analyzed": 162,
        "matches_processed": 12543,
        "players_tracked": 892,
        "api_calls": 15678
    },
    "demo_champions": [
        {"name": "阿狸", "win_rate": 52.3, "pick_rate": 15.2, "tier": "S", "role": "中单", "icon": "🦊"},
        {"name": "劫", "win_rate": 49.8, "pick_rate": 12.7, "tier": "A+", "role": "中单", "icon": "🗡️"},
        {"name": "金克丝", "win_rate": 51.2, "pick_rate": 18.4, "tier": "S", "role": "ADC", "icon": "🎯"},
        {"name": "盖伦", "win_rate": 50.1, "pick_rate": 8.9, "tier": "B+", "role": "上单", "icon": "⚔️"},
        {"name": "拉克丝", "win_rate": 53.4, "pick_rate": 22.1, "tier": "S+", "role": "辅助", "icon": "✨"}
    ]
}

@app.route('/')
def home():
    """美化版主页"""
    return render_template('index_beautiful.html', 
                         data=BEAUTIFUL_DATA,
                         timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/github')
def github():
    """美化版GitHub页面"""
    projects = [
        {"name": "riotwatcher", "desc": "Python Riot API包装器", "stars": "1.2k", "lang": "Python", "url": "#"},
        {"name": "cassiopeia", "desc": "高级LoL数据框架", "stars": "500+", "lang": "Python", "url": "#"},
        {"name": "lol-js", "desc": "JavaScript API客户端", "stars": "300+", "lang": "JavaScript", "url": "#"},
        {"name": "lolcat", "desc": "命令行数据工具", "stars": "200+", "lang": "Go", "url": "#"}
    ]
    return render_template('github_beautiful.html', 
                         projects=projects,
                         count=len(projects))

@app.route('/api/health')
def health():
    return jsonify({
        "status": "online",
        "service": "LoL Analytics Platform",
        "version": "2.0-beautiful",
        "uptime": "100%",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/demo/faker')
def demo_faker():
    return jsonify({
        "player": {
            "name": "Faker",
            "real_name": "李相赫",
            "team": "T1",
            "position": "Mid",
            "achievements": ["3×世界冠军", "10×LCK冠军", "传奇选手"]
        },
        "stats": {
            "career_wins": 700,
            "champion_pool": 92,
            "mvp_awards": 45
        }
    })

@app.route('/about')
def about():
    return render_template('about_beautiful.html')

if __name__ == '__main__':
    print("🚀 启动美化版应用...")
    app.run(debug=True)
