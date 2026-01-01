"""
作业专用简化版 - 针对PythonAnywhere优化
保持GitHub仓库中的完整代码，但运行这个简化版
"""
from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# 演示数据路径
DEMO_DATA_FILE = "data/demo_data.json"

def load_demo_data():
    """加载演示数据"""
    try:
        with open(DEMO_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"error": "演示数据未生成，请运行 generate_demo_data.py"}

@app.route('/')
def home():
    """主页 - 展示项目功能"""
    data = load_demo_data()
    return render_template('index_simple.html', 
                         data=data,
                         timestamp=datetime.now().isoformat())

@app.route('/api/data')
def api_data():
    """数据API"""
    return jsonify(load_demo_data())

@app.route('/api/demo/faker')
def demo_faker():
    """Faker示例数据"""
    return jsonify({
        "name": "Faker (李相赫)",
        "team": "T1",
        "region": "KR",
        "achievements": ["3× World Champion", "10× LCK Champion"],
        "demo_note": "这是演示数据，真实数据需要Riot API调用"
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "online",
        "service": "LoL Data Analysis (Demo Mode)",
        "timestamp": datetime.now().isoformat(),
        "cpu_safe": True
    })

if __name__ == '__main__':
    # 检查必要文件
    if not os.path.exists(DEMO_DATA_FILE):
        print("⚠️  请先运行: python generate_demo_data.py")
    
    app.run(debug=True)
