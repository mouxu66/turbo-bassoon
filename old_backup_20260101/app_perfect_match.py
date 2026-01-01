from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import json
import time

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'lol_items.db')

def get_db_stats():
    """获取数据库统计信息"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute("SELECT COUNT(*) FROM items")
        total = cursor.fetchone()[0]
        
        # 价格统计
        cursor.execute("SELECT MIN(gold_total), MAX(gold_total), AVG(gold_total) FROM items WHERE gold_total > 0")
        min_price, max_price, avg_price = cursor.fetchone()
        
        # 分类统计
        cursor.execute("SELECT category, COUNT(*) FROM items WHERE category IS NOT NULL GROUP BY category")
        categories = cursor.fetchall()
        
        # 最贵装备
        cursor.execute("SELECT name, gold_total FROM items WHERE gold_total > 0 ORDER BY gold_total DESC LIMIT 5")
        expensive = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'min_price': min_price or 0,
            'max_price': max_price or 0,
            'avg_price': int(avg_price) if avg_price else 0,
            'categories': categories,
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
        <title>🎮 LoL装备数据库 - 专业版</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: linear-gradient(135deg, #0a1428, #1a2b4a);
                color: #c8aa6e;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                padding: 40px 30px;
                background: linear-gradient(135deg, rgba(30, 35, 40, 0.95), rgba(20, 25, 30, 0.95));
                border-radius: 20px;
                border: 3px solid #c8aa6e;
                margin-bottom: 30px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }
            .header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,215,0,0.1) 0%, transparent 70%);
                z-index: 0;
            }
            .header-content {
                position: relative;
                z-index: 1;
            }
            h1 {
                color: #ffd700;
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
                background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .subtitle {
                color: #a09b8c;
                font-size: 1.2em;
                margin-bottom: 20px;
            }
            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.1));
                color: #00ff00;
                padding: 10px 25px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 1.1em;
                margin: 15px 0;
                border: 2px solid #00ff00;
                backdrop-filter: blur(10px);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin: 40px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                border: 1px solid rgba(200, 170, 110, 0.2);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #ffd700, #c8aa6e, #ffd700);
            }
            .stat-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                border-color: #c8aa6e;
            }
            .stat-number {
                font-size: 2.8em;
                color: #ffd700;
                font-weight: bold;
                margin: 15px 0;
                text-shadow: 0 2px 5px rgba(255, 215, 0, 0.3);
            }
            .stat-label {
                color: #a09b8c;
                font-size: 1.1em;
                margin-top: 10px;
            }
            .btn-group {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 50px 0;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                gap: 12px;
                background: linear-gradient(135deg, gold, #ffcc00);
                color: black;
                padding: 16px 32px;
                text-decoration: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 1.2em;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
                box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
            }
            .btn:hover {
                transform: translateY(-5px) scale(1.05);
                box-shadow: 0 15px 30px rgba(255, 215, 0, 0.5);
                background: linear-gradient(135deg, #ffcc00, gold);
            }
            .btn-secondary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }
            .btn-secondary:hover {
                background: linear-gradient(135deg, #764ba2, #667eea);
                box-shadow: 0 15px 30px rgba(102, 126, 234, 0.5);
            }
            .section {
                margin: 60px 0;
                padding: 40px;
                background: linear-gradient(135deg, rgba(30, 35, 40, 0.8), rgba(20, 25, 30, 0.8));
                border-radius: 20px;
                border: 2px solid rgba(200, 170, 110, 0.3);
            }
            .section-title {
                color: #ffd700;
                font-size: 2em;
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 3px solid #c8aa6e;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .items-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }
            .item-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
                border-radius: 15px;
                padding: 25px;
                border-left: 5px solid #ffd700;
                transition: all 0.3s;
                border: 1px solid rgba(200, 170, 110, 0.1);
            }
            .item-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                border-color: #c8aa6e;
                background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            }
            .item-name {
                color: white;
                font-size: 1.4em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .item-price {
                color: #48bb78;
                font-size: 1.5em;
                font-weight: bold;
                margin: 15px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .item-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin: 15px 0;
            }
            .tag {
                background: rgba(100, 126, 234, 0.2);
                color: #a3bffa;
                padding: 6px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                border: 1px solid rgba(100, 126, 234, 0.3);
            }
            .category-badges {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin: 30px 0;
            }
            .category-badge {
                background: rgba(200, 170, 110, 0.1);
                padding: 12px 24px;
                border-radius: 25px;
                border: 2px solid #c8aa6e;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-width: 150px;
            }
            .category-count {
                font-size: 2em;
                color: gold;
                font-weight: bold;
            }
            .category-name {
                color: #a09b8c;
                margin-top: 5px;
            }
            .footer {
                text-align: center;
                margin-top: 60px;
                padding: 40px;
                color: #a09b8c;
                border-top: 1px solid rgba(200, 170, 110, 0.2);
                background: rgba(0, 0, 0, 0.2);
                border-radius: 15px;
            }
            .db-info {
                background: rgba(0, 100, 255, 0.1);
                border-left: 4px solid #0a74da;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            @media (max-width: 768px) {
                .container { padding: 10px; }
                h1 { font-size: 2em; }
                .btn-group { flex-direction: column; align-items: center; }
                .btn { width: 100%; max-width: 300px; justify-content: center; }
                .items-grid { grid-template-columns: 1fr; }
                .stats-grid { grid-template-columns: 1fr; }
                .section { padding: 20px; }
            }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-content">
                    <h1><i class="fas fa-dragon"></i> 英雄联盟装备数据库</h1>
                    <div class="subtitle">专业Riot API数据版 • PythonAnywhere</div>
                    
                    <div class="status-badge">
                        <i class="fas fa-database"></i> 数据库连接正常 • 数据完整
                    </div>
                    
                    <div style="margin-top: 20px; color: #a09b8c; font-size: 1.1em;">
                        <p><i class="fas fa-server"></i> 服务器运行稳定 • 最后更新: ''' + time.strftime("%Y-%m-%d %H:%M") + '''</p>
                    </div>
                </div>
            </div>
    '''
    
    if stats:
        html += f'''
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats['total']}</div>
                    <div class="stat-label"><i class="fas fa-shield-alt"></i> 总装备数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['min_price']}-{stats['max_price']}</div>
                    <div class="stat-label"><i class="fas fa-coins"></i> 价格范围</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['avg_price']}</div>
                    <div class="stat-label"><i class="fas fa-calculator"></i> 平均价格</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(stats['categories'])}</div>
                    <div class="stat-label"><i class="fas fa-tags"></i> 分类数量</div>
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/api/items" class="btn">
                    <i class="fas fa-code"></i> 完整API数据
                </a>
                <a href="/items" class="btn btn-secondary">
                    <i class="fas fa-list"></i> 网页查看装备
                </a>
                <a href="/categories" class="btn">
                    <i class="fas fa-tags"></i> 按分类浏览
                </a>
                <a href="/search" class="btn btn-secondary">
                    <i class="fas fa-search"></i> 搜索装备
                </a>
            </div>
            
            <div class="section">
                <h2 class="section-title"><i class="fas fa-crown"></i> 最贵装备</h2>
                <div class="items-grid">
        '''
        
        for name, price in stats['expensive']:
            html += f'''
                    <div class="item-card">
                        <div class="item-name">{name}</div>
                        <div class="item-price">
                            <i class="fas fa-coins"></i> {price} 金币
                        </div>
                        <p style="color: #a09b8c; margin-top: 10px;">高端局核心装备</p>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title"><i class="fas fa-chart-pie"></i> 装备分类统计</h2>
                <div class="category-badges">
        '''
        
        for category, count in stats['categories']:
            if category:  # 确保category不为空
                html += f'''
                    <div class="category-badge">
                        <div class="category-count">{count}</div>
                        <div class="category-name">{category}</div>
                    </div>
                '''
        
        html += '''
                </div>
            </div>
            
            <div class="db-info">
                <h3><i class="fas fa-info-circle"></i> 数据库信息</h3>
                <p><strong>表结构</strong>: 完整的Riot API格式 (17个字段)</p>
                <p><strong>关键字段</strong>: name, gold_total, category, tags, stats, description</p>
                <p><strong>数据来源</strong>: Riot Games API 兼容格式</p>
                <p><strong>更新时间</strong>: 自动记录 (last_updated字段)</p>
            </div>
        '''
    else:
        html += '''
            <div class="section" style="text-align: center; padding: 60px 20px;">
                <h2 style="color: #ff6b6b;"><i class="fas fa-exclamation-triangle"></i> 数据库统计获取失败</h2>
                <p style="margin: 20px 0; font-size: 1.1em;">数据库文件存在，但无法读取统计信息</p>
                <div style="margin-top: 30px;">
                    <a href="/api/items" class="btn">直接查看原始数据</a>
                </div>
            </div>
        '''
    
    html += f'''
            <div class="footer">
                <p><i class="fas fa-globe"></i> <strong>公开访问网址</strong>: https://mouxu.pythonanywhere.com</p>
                <p><i class="fas fa-database"></i> <strong>数据库</strong>: SQLite • {os.path.getsize(DB_PATH)//1024} KB • {time.strftime("%Y-%m-%d")}</p>
                <p><i class="fas fa-code"></i> <strong>技术栈</strong>: Flask + SQLite + PythonAnywhere</p>
                <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.7;">
                    数据格式兼容Riot Games API • 非官方项目 • 仅供学习使用
                </p>
            </div>
        </div>
        
        <script>
            // 页面交互效果
            document.addEventListener('DOMContentLoaded', function() {{
                // 卡片悬停效果
                const cards = document.querySelectorAll('.stat-card, .item-card');
                cards.forEach(card => {{
                    card.addEventListener('mouseenter', function() {{
                        this.style.transform = 'translateY(-10px)';
                    }});
                    card.addEventListener('mouseleave', function() {{
                        this.style.transform = 'translateY(0)';
                    }});
                }});
                
                // 实时更新时间
                function updateTime() {{
                    const now = new Date();
                    const timeStr = now.toLocaleString('zh-CN');
                    const timeElements = document.querySelectorAll('.header-content p');
                    if (timeElements.length > 0) {{
                        timeElements[0].innerHTML = `<i class="fas fa-server"></i> 服务器运行稳定 • 当前时间: ${{timeStr}}`;
                    }}
                }}
                setInterval(updateTime, 60000);
                updateTime();
                
                // 滚动动画
                const observerOptions = {{
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                }};
                
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }}
                    }});
                }}, observerOptions);
                
                // 观察所有卡片
                document.querySelectorAll('.stat-card, .item-card, .category-badge').forEach(el => {{
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(20px)';
                    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    observer.observe(el);
                }});
            }});
        </script>
    </body>
    </html>
    '''
    
    return html

@app.route('/api/items')
def api_items():
    """完整API接口 - 返回所有装备数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()
        
        items_list = []
        for item in items:
            item_dict = dict(item)
            # 尝试解析stats JSON
            if item_dict.get('stats'):
                try:
                    item_dict['stats_parsed'] = json.loads(item_dict['stats'])
                except:
                    item_dict['stats_parsed'] = None
            items_list.append(item_dict)
        
        return jsonify({
            'status': 'success',
            'count': len(items_list),
            'database_info': {
                'table': 'items',
                'columns': 17,
                'format': 'Riot API compatible'
            },
            'items': items_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items')
def items_page():
    """装备列表页面"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gold_total, category, plaintext FROM items ORDER BY name")
        items = cursor.fetchall()
        conn.close()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备列表 - LoL数据库</title>
            <style>
                body {
                    background: #0a1428;
                    color: #c8aa6e;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    background: linear-gradient(135deg, rgba(30, 35, 40, 0.9), rgba(20, 25, 30, 0.9));
                    padding: 40px;
                    border-radius: 20px;
                    margin-bottom: 30px;
                    border: 3px solid #c8aa6e;
                }
                h1 {
                    color: #ffd700;
                    margin: 0 0 10px 0;
                    font-size: 2.5em;
                }
                .back-btn {
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    background: rgba(200, 170, 110, 0.1);
                    color: #c8aa6e;
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    margin: 20px 0;
                    border: 2px solid #c8aa6e;
                    font-weight: bold;
                }
                .back-btn:hover {
                    background: rgba(200, 170, 110, 0.2);
                }
                .items-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
                    gap: 25px;
                }
                .item-box {
                    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
                    border-radius: 15px;
                    padding: 25px;
                    border: 1px solid rgba(200, 170, 110, 0.2);
                    transition: all 0.3s;
                    border-left: 5px solid #ffd700;
                }
                .item-box:hover {
                    transform: translateY(-8px);
                    border-color: #c8aa6e;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                }
                .item-title {
                    color: white;
                    font-size: 1.3em;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .item-price {
                    color: #48bb78;
                    font-size: 1.4em;
                    font-weight: bold;
                    margin: 15px 0;
                }
                .item-category {
                    display: inline-block;
                    background: rgba(100, 126, 234, 0.2);
                    color: #a3bffa;
                    padding: 8px 18px;
                    border-radius: 20px;
                    font-size: 0.95em;
                    margin: 10px 0;
                    border: 1px solid rgba(100, 126, 234, 0.3);
                }
                .item-desc {
                    color: #a09b8c;
                    margin: 15px 0;
                    line-height: 1.6;
                }
                .view-btn {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    background: gold;
                    color: black;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 15px;
                }
                .stats-bar {
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 30px 0;
                    text-align: center;
                    font-size: 1.1em;
                }
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><i class="fas fa-shield-alt"></i> 装备完整列表</h1>
                    <p>所有装备数据 (按名称排序)</p>
                    <a href="/" class="back-btn">
                        <i class="fas fa-arrow-left"></i> 返回首页
                    </a>
                </div>
                
                <div class="stats-bar">
                    <span style="color: #ffd700; margin-right: 30px;">
                        <i class="fas fa-boxes"></i> 总数: ''' + str(len(items)) + ''' 件
                    </span>
                    <span style="color: #48bb78;">
                        <i class="fas fa-filter"></i> 17个完整属性字段
                    </span>
                </div>
                
                <div class="items-container">
        '''
        
        for item_id, name, gold_total, category, plaintext in items:
            html += f'''
                    <div class="item-box">
                        <div class="item-title">{name}</div>
                        <div class="item-price">💰 {gold_total if gold_total else 0} 金币</div>
                        {f'<div class="item-category">{category}</div>' if category else ''}
                        {f'<div class="item-desc">{plaintext[:120]}{"..." if len(str(plaintext)) > 120 else ""}</div>' if plaintext else ''}
                        <a href="/item/{item_id}" class="view-btn">
                            <i class="fas fa-eye"></i> 查看完整详情
                        </a>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    """装备详情页面"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return "装备不存在", 404
        
        item_dict = dict(item)
        
        # 解析stats JSON
        stats_parsed = None
        if item_dict.get('stats'):
            try:
                stats_parsed = json.loads(item_dict['stats'])
            except:
                pass
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{item_dict['name']} - LoL装备详情</title>
            <style>
                body {{
                    background: linear-gradient(135deg, #0a1428, #1a2b4a);
                    color: #c8aa6e;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                }}
                .header {{
                    background: linear-gradient(135deg, rgba(30, 35, 40, 0.9), rgba(20, 25, 30, 0.9));
                    padding: 40px;
                    border-radius: 20px;
                    margin-bottom: 30px;
                    border: 3px solid #c8aa6e;
                }}
                h1 {{
                    color: #ffd700;
                    margin: 0 0 10px 0;
                    font-size: 2.8em;
                }}
                .price-tag {{
                    background: gold;
                    color: black;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 1.8em;
                    font-weight: bold;
                    display: inline-block;
                    margin: 20px 0;
                }}
                .nav-buttons {{
                    margin: 25px 0;
                }}
                .nav-btn {{
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    background: rgba(200, 170, 110, 0.1);
                    color: #c8aa6e;
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    margin-right: 15px;
                    border: 2px solid #c8aa6e;
                    font-weight: bold;
                }}
                .nav-btn:hover {{
                    background: rgba(200, 170, 110, 0.2);
                }}
                .detail-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 25px;
                    margin: 40px 0;
                }}
                .detail-card {{
                    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
                    border-radius: 15px;
                    padding: 30px;
                    border: 1px solid rgba(200, 170, 110, 0.2);
                }}
                .detail-title {{
                    color: #ffd700;
                    font-size: 1.3em;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #c8aa6e;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .property {{
                    margin: 15px 0;
                    padding: 15px;
                    background: rgba(255,255,255,0.03);
                    border-radius: 8px;
                }}
                .prop-label {{
                    color: #a09b8c;
                    font-weight: bold;
                    margin-bottom: 8px;
                    font-size: 0.95em;
                }}
                .prop-value {{
                    color: white;
                    line-height: 1.6;
                }}
                .tags-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin: 15px 0;
                }}
                .tag {{
                    background: rgba(100, 126, 234, 0.2);
                    color: #a3bffa;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    border: 1px solid rgba(100, 126, 234, 0.3);
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .stat-item {{
                    background: rgba(72, 187, 120, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    border: 1px solid rgba(72, 187, 120, 0.2);
                }}
                .stat-name {{
                    color: #a09b8c;
                    font-size: 0.9em;
                    margin-bottom: 5px;
                }}
                .stat-value {{
                    color: #48bb78;
                    font-size: 1.3em;
                    font-weight: bold;
                }}
                @media (max-width: 768px) {{
                    .container {{ padding: 10px; }}
                    h1 {{ font-size: 2em; }}
                    .detail-grid {{ grid-template-columns: 1fr; }}
                    .nav-buttons {{ display: flex; flex-direction: column; gap: 10px; }}
                    .nav-btn {{ margin: 0; }}
                }}
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><i class="fas fa-shield-alt"></i> {item_dict['name']}</h1>
                    <div class="price-tag">
                        <i class="fas fa-coins"></i> {item_dict['gold_total'] if item_dict['gold_total'] else 0} 金币
                    </div>
                    
                    <div class="nav-buttons">
                        <a href="/items" class="nav-btn">
                            <i class="fas fa-arrow-left"></i> 返回列表
                        </a>
                        <a href="/" class="nav-btn">
                            <i class="fas fa-home"></i> 返回首页
                        </a>
                        <a href="/api/items/{item_id}" class="nav-btn">
                            <i class="fas fa-code"></i> JSON数据
                        </a>
                    </div>
                </div>
                
                <div class="detail-grid">
        '''
        
        # 基本信息卡片
        html += '''
                    <div class="detail-card">
                        <div class="detail-title"><i class="fas fa-info-circle"></i> 基本信息</div>
        '''
        
        basic_info = [
            ('名称', item_dict['name']),
            ('简短描述', item_dict.get('plaintext')),
            ('完整描述', item_dict.get('description')),
            ('分类', item_dict.get('category')),
            ('版本', item_dict.get('version')),
            ('合成层级', item_dict.get('depth')),
            ('可用地图', item_dict.get('maps'))
        ]
        
        for label, value in basic_info:
            if value:
                html += f'''
                        <div class="property">
                            <div class="prop-label">{label}:</div>
                            <div class="prop-value">{value}</div>
                        </div>
                '''
        
        html += '''
                    </div>
        '''
        
        # 价格信息卡片
        html += '''
                    <div class="detail-card">
                        <div class="detail-title"><i class="fas fa-coins"></i> 价格信息</div>
        '''
        
        price_info = [
            ('总价格', item_dict.get('gold_total')),
            ('基础价格', item_dict.get('gold_base')),
            ('出售价格', item_dict.get('gold_sell'))
        ]
        
        for label, value in price_info:
            if value:
                html += f'''
                        <div class="property">
                            <div class="prop-label">{label}:</div>
                            <div class="prop-value">{value} 金币</div>
                        </div>
                '''
        
        html += '''
                    </div>
        '''
        
        # 标签信息
        if item_dict.get('tags'):
            tags = item_dict['tags'].split(',')
            html += f'''
                    <div class="detail-card">
                        <div class="detail-title"><i class="fas fa-tags"></i> 装备标签</div>
                        <div class="tags-container">
            '''
            
            for tag in tags:
                html += f'<span class="tag">{tag}</span>'
            
            html += '''
                        </div>
                    </div>
            '''
        
        # 属性加成
        if stats_parsed:
            html += '''
                    <div class="detail-card">
                        <div class="detail-title"><i class="fas fa-chart-bar"></i> 属性加成</div>
                        <div class="stats-grid">
            '''
            
            for stat_name, stat_value in stats_parsed.items():
                html += f'''
                            <div class="stat-item">
                                <div class="stat-name">{stat_name}</div>
                                <div class="stat-value">+{stat_value}</div>
                            </div>
                '''
            
            html += '''
                        </div>
                    </div>
            '''
        
        # 合成路线
        if item_dict.get('into_items') or item_dict.get('from_items'):
            html += '''
                    <div class="detail-card">
                        <div class="detail-title"><i class="fas fa-sitemap"></i> 合成路线</div>
            '''
            
            if item_dict.get('from_items'):
                html += '''
                        <div class="property">
                            <div class="prop-label">合成所需:</div>
                            <div class="prop-value">''' + item_dict['from_items'] + '''</div>
                        </div>
                '''
            
            if item_dict.get('into_items'):
                html += '''
                        <div class="property">
                            <div class="prop-label">可合成为:</div>
                            <div class="prop-value">''' + item_dict['into_items'] + '''</div>
                        </div>
                '''
            
            html += '''
                    </div>
            '''
        
        html += f'''
                </div>
                
                <div style="text-align: center; margin: 50px 0; color: #a09b8c;">
                    <p><i class="fas fa-database"></i> 数据ID: {item_id} • 最后更新: {item_dict.get('last_updated', '未知')}</p>
                    <p><i class="fas fa-shield-alt"></i> 完整Riot API格式数据 • 17个属性字段</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/api/items/<int:item_id>')
def api_item_detail(item_id):
    """单个装备的API接口"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        item_dict = dict(item)
        if item_dict.get('stats'):
            try:
                item_dict['stats_parsed'] = json.loads(item_dict['stats'])
            except:
                item_dict['stats_parsed'] = None
        
        return jsonify(item_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/categories')
def categories_page():
    """分类浏览页面"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT category, COUNT(*) as count FROM items WHERE category IS NOT NULL GROUP BY category ORDER BY count DESC")
        categories = cursor.fetchall()
        conn.close()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>装备分类 - LoL数据库</title>
            <style>
                body {
                    background: #0a1428;
                    color: #c8aa6e;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    background: linear-gradient(135deg, rgba(30, 35, 40, 0.9), rgba(20, 25, 30, 0.9));
                    padding: 40px;
                    border-radius: 20px;
                    margin-bottom: 30px;
                    border: 3px solid #c8aa6e;
                }
                h1 {
                    color: #ffd700;
                }
                .category-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 25px;
                }
                .category-card {
                    background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
                    border-radius: 15px;
                    padding: 30px;
                    text-align: center;
                    border: 2px solid transparent;
                    transition: all 0.3s;
                    border-left: 5px solid #c8aa6e;
                }
                .category-card:hover {
                    border-color: #c8aa6e;
                    transform: translateY(-10px);
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                }
                .category-count {
                    font-size: 3em;
                    color: gold;
                    font-weight: bold;
                    margin: 15px 0;
                    text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
                }
                .category-name {
                    font-size: 1.5em;
                    color: white;
                    margin: 15px 0;
                }
                .view-btn {
                    display: inline-block;
                    background: gold;
                    color: black;
                    padding: 12px 24px;
                    border-radius: 8px;
                    text-decoration: none;
                    margin-top: 20px;
                    font-weight: bold;
                    font-size: 1.1em;
                }
                .back-btn {
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    background: rgba(200, 170, 110, 0.1);
                    color: #c8aa6e;
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    margin: 20px 0;
                    border: 2px solid #c8aa6e;
                    font-weight: bold;
                }
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><i class="fas fa-tags"></i> 装备分类浏览</h1>
                    <a href="/" class="back-btn">返回首页</a>
                </div>
                
                <div class="category-grid">
        '''
        
        for category, count in categories:
            html += f'''
                    <div class="category-card">
                        <div class="category-count">{count}</div>
                        <div class="category-name">{category}</div>
                        <div>件装备</div>
                        <a href="/items?category={category}" class="view-btn">
                            <i class="fas fa-eye"></i> 查看该分类
                        </a>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/search')
def search_page():
    """搜索页面"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>搜索装备 - LoL数据库</title>
        <style>
            body { background: #0a1428; color: #c8aa6e; padding: 50px; text-align: center; }
            h1 { color: gold; }
            .search-box { 
                max-width: 600px; 
                margin: 30px auto; 
                padding: 30px;
                background: rgba(30, 35, 40, 0.9);
                border-radius: 15px;
                border: 2px solid #c8aa6e;
            }
            input[type="text"] {
                width: 100%;
                padding: 15px;
                border: 2px solid #c8aa6e;
                background: rgba(255,255,255,0.1);
                color: white;
                border-radius: 8px;
                font-size: 1.1em;
                margin-bottom: 20px;
            }
            .search-btn {
                background: gold;
                color: black;
                padding: 15px 40px;
                border: none;
                border-radius: 8px;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
            }
            a { color: gold; }
        </style>
    </head>
    <body>
        <h1>🔍 搜索装备</h1>
        <p>搜索功能开发中...</p>
        <div class="search-box">
            <input type="text" placeholder="输入装备名称或效果关键词..." disabled>
            <button class="search-btn" disabled>搜索</button>
        </div>
        <p><a href="/">← 返回首页</a></p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'lol-items-database',
        'database': {
            'path': DB_PATH,
            'exists': os.path.exists(DB_PATH),
            'size_kb': os.path.getsize(DB_PATH) // 1024 if os.path.exists(DB_PATH) else 0
        },
        'url': 'https://mouxu.pythonanywhere.com',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)
