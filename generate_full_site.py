# /home/mouxu/generate_full_site.py
import os
import sqlite3
import json
import csv
from datetime import datetime
from pathlib import Path

def generate_complete_site():
    """生成完整的静态网站"""
    
    base_dir = Path("/home/mouxu")
    docs_dir = base_dir / "docs"
    project_dir = base_dir / "project"
    
    print("🚀 生成完整英雄联盟数据分析网站...")
    
    # 创建目录结构
    (docs_dir / "items").mkdir(exist_ok=True)
    (docs_dir / "analysis").mkdir(exist_ok=True)
    (docs_dir / "data").mkdir(exist_ok=True)
    (docs_dir / "assets").mkdir(exist_ok=True)
    
    # 1. 生成首页
    generate_index(docs_dir, project_dir)
    
    # 2. 生成装备页面
    generate_items_pages(docs_dir, project_dir)
    
    # 3. 生成比赛分析页面
    generate_analysis_pages(docs_dir, project_dir)
    
    # 4. 生成数据文件
    generate_data_files(docs_dir, project_dir)
    
    # 5. 生成关于页面
    generate_about_page(docs_dir)
    
    print(f"✅ 网站生成完成！保存到: {docs_dir}")

def generate_index(docs_dir, project_dir):
    """生成首页"""
    
    # 检查数据库
    db_path = project_dir / "instance" / "lol_data.db"
    has_db = db_path.exists()
    
    if has_db:
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM items")
            item_count = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM matches")
            match_count = cursor.fetchone()[0] or 0
            conn.close()
        except:
            item_count = 0
            match_count = 0
    else:
        item_count = 0
        match_count = 0
    
    html = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>英雄联盟数据分析 - 完整版</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary: #4a6bdf;
            --secondary: #6c5ce7;
            --accent: #fd79a8;
        }}
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            font-family: 'Microsoft YaHei', sans-serif;
        }}
        .navbar-brand {{
            font-weight: bold;
            font-size: 1.5rem;
        }}
        .hero-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 50px;
            margin-top: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s;
            height: 100%;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .stat-icon {{
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: var(--primary);
        }}
        .feature-list li {{
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .feature-list li:last-child {{
            border-bottom: none;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 50px;
            padding: 20px;
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
            color: white;
        }}
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-trophy"></i> LOL数据分析
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">首页</a></li>
                    <li class="nav-item"><a class="nav-link" href="/items/">装备数据</a></li>
                    <li class="nav-item"><a class="nav-link" href="/analysis/">比赛分析</a></li>
                    <li class="nav-item"><a class="nav-link" href="/data/">数据下载</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://mouxu.pythonanywhere.com" target="_blank">
                        <i class="fas fa-bolt"></i> 动态版本
                    </a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- 主要内容 -->
    <div class="container">
        <div class="hero-section">
            <div class="text-center mb-5">
                <h1 class="display-4 fw-bold mb-3">🏆 英雄联盟数据分析平台</h1>
                <p class="lead text-muted">基于PythonAnywhere + GitHub Pages的完整数据解决方案</p>
            </div>
            
            <!-- 统计卡片 -->
            <div class="row mb-5">
                <div class="col-md-3 mb-4">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h3>{item_count}</h3>
                        <p class="text-muted">装备数量</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-gamepad"></i>
                        </div>
                        <h3>{match_count}</h3>
                        <p class="text-muted">比赛记录</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-database"></i>
                        </div>
                        <h3>{(item_count + match_count) or 0}</h3>
                        <p class="text-muted">总数据量</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-sync-alt"></i>
                        </div>
                        <h3>24/7</h3>
                        <p class="text-muted">自动更新</p>
                    </div>
                </div>
            </div>
            
            <!-- 功能简介 -->
            <div class="row mb-5">
                <div class="col-md-6">
                    <h3 class="mb-4"><i class="fas fa-star text-warning"></i> 主要功能</h3>
                    <ul class="feature-list list-unstyled">
                        <li><i class="fas fa-check text-success me-2"></i> 装备属性查询与分析</li>
                        <li><i class="fas fa-check text-success me-2"></i> 比赛数据统计与可视化</li>
                        <li><i class="fas fa-check text-success me-2"></i> CSV文件上传与处理</li>
                        <li><i class="fas fa-check text-success me-2"></i> 数据导出与分享</li>
                        <li><i class="fas fa-check text-success me-2"></i> 多版本数据对比</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h3 class="mb-4"><i class="fas fa-cogs text-info"></i> 技术特性</h3>
                    <ul class="feature-list list-unstyled">
                        <li><i class="fas fa-server me-2"></i> Flask + SQLite后端</li>
                        <li><i class="fas fa-desktop me-2"></i> Bootstrap 5前端</li>
                        <li><i class="fas fa-cloud me-2"></i> GitHub Pages自动部署</li>
                        <li><i class="fas fa-bolt me-2"></i> PythonAnywhere动态处理</li>
                        <li><i class="fas fa-mobile-alt me-2"></i> 响应式设计</li>
                    </ul>
                </div>
            </div>
            
            <!-- 行动按钮 -->
            <div class="text-center">
                <a href="/items/" class="btn btn-primary btn-lg me-3">
                    <i class="fas fa-search"></i> 浏览装备数据
                </a>
                <a href="/analysis/" class="btn btn-outline-primary btn-lg me-3">
                    <i class="fas fa-chart-bar"></i> 查看比赛分析
                </a>
                <a href="https://mouxu.pythonanywhere.com" target="_blank" class="btn btn-success btn-lg">
                    <i class="fas fa-upload"></i> 上传新数据
                </a>
            </div>
        </div>
        
        <!-- 双站说明 -->
        <div class="row mt-5">
            <div class="col-12">
                <div class="alert alert-info">
                    <h4><i class="fas fa-sitemap"></i> 双站协作架构说明</h4>
                    <p class="mb-0">
                        <strong>GitHub Pages（当前站点）</strong>: 静态展示，快速访问，数据分析结果展示<br>
                        <strong>PythonAnywhere（动态站点）</strong>: 数据上传，实时处理，完整功能操作<br>
                        数据自动同步，提供无缝用户体验
                    </p>
                </div>
            </div>
        </div>
        
        <!-- 页脚 -->
        <div class="footer text-center">
            <p>© 2024 英雄联盟数据分析平台 | 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p class="small">
                <a href="https://github.com/mouxu66/turbo-bassoon" class="text-white me-3"><i class="fab fa-github"></i> GitHub仓库</a>
                <a href="https://mouxu.pythonanywhere.com" class="text-white me-3"><i class="fas fa-external-link-alt"></i> 动态版本</a>
                <a href="/about/" class="text-white"><i class="fas fa-info-circle"></i> 关于项目</a>
            </p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 简单交互效果
        document.addEventListener('DOMContentLoaded', function() {{
            // 统计卡片动画
            const stats = document.querySelectorAll('.stat-card h3');
            stats.forEach(stat => {{
                const target = parseInt(stat.textContent);
                if (!isNaN(target) && target > 0) {{
                    let current = 0;
                    const increment = target / 50;
                    const timer = setInterval(() => {{
                        current += increment;
                        if (current >= target) {{
                            current = target;
                            clearInterval(timer);
                        }}
                        stat.textContent = Math.floor(current);
                    }}, 30);
                }}
            }});
        }});
    </script>
</body>
</html>
'''
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 首页生成完成")

def generate_items_pages(docs_dir, project_dir):
    """生成装备数据页面"""
    
    # 检查CSV文件
    csv_files = []
    for csv_file in ["ItemTbl.csv", "LOL_items_stats.csv"]:
        csv_path = project_dir / csv_file
        if csv_path.exists():
            csv_files.append(csv_file)
    
    # 检查数据库
    db_path = project_dir / "instance" / "lol_data.db"
    items_data = []
    
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name, gold_total, ad, ap, health, armor, mr FROM items LIMIT 50")
            items_data = [dict(row) for row in cursor.fetchall()]
            conn.close()
        except:
            items_data = []
    
    # 生成主页面
    items_html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>装备数据 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item active">装备数据</li>
            </ol>
        </nav>
        
        <h1 class="mb-4"><i class="fas fa-shield-alt"></i> 英雄联盟装备数据库</h1>
        
        <div class="alert alert-info">
            <h5><i class="fas fa-info-circle"></i> 数据来源</h5>
            <p class="mb-2">可用数据文件: {len(csv_files)}个</p>
            {''.join([f'<span class="badge bg-secondary me-2">{file}</span>' for file in csv_files])}
            <p class="mt-2 mb-0">装备总数: {len(items_data)}件</p>
        </div>
        
        {generate_items_table(items_data)}
        
        <div class="mt-4">
            <a href="/" class="btn btn-outline-primary">
                <i class="fas fa-home"></i> 返回首页
            </a>
            <a href="/analysis/" class="btn btn-primary ms-2">
                <i class="fas fa-chart-bar"></i> 查看比赛分析
            </a>
            <a href="https://mouxu.pythonanywhere.com/items" target="_blank" class="btn btn-success ms-2">
                <i class="fas fa-external-link-alt"></i> 完整装备查询
            </a>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    <script>
        $(document).ready(function() {{
            $('#itemsTable').DataTable({{
                pageLength: 25,
                language: {{
                    url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/zh-CN.json'
                }}
            }});
        }});
    </script>
</body>
</html>
'''
    
    with open(docs_dir / "items" / "index.html", "w", encoding="utf-8") as f:
        f.write(items_html)
    
    # 生成详细的装备页面（如果数据量大可以分页）
    for i, item in enumerate(items_data[:20]):
        item_html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>{item.get('name', '装备详情')} - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item"><a href="/items/">装备数据</a></li>
                <li class="breadcrumb-item active">装备详情</li>
            </ol>
        </nav>
        
        <div class="card">
            <div class="card-header">
                <h2 class="mb-0">{item.get('name', '未知装备')}</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h5>基础属性</h5>
                        <ul class="list-unstyled">
                            <li><strong>价格:</strong> <span class="badge bg-warning">{item.get('gold_total', 0)} 金币</span></li>
                            <li><strong>攻击力:</strong> {item.get('ad', 0)}</li>
                            <li><strong>法术强度:</strong> {item.get('ap', 0)}</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h5>防御属性</h5>
                        <ul class="list-unstyled">
                            <li><strong>生命值:</strong> {item.get('health', 0)}</li>
                            <li><strong>护甲:</strong> {item.get('armor', 0)}</li>
                            <li><strong>魔法抗性:</strong> {item.get('mr', 0)}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <a href="/items/" class="btn btn-outline-primary">返回装备列表</a>
        </div>
    </div>
</body>
</html>
'''
        with open(docs_dir / "items" / f"item_{i+1}.html", "w", encoding="utf-8") as f:
            f.write(item_html)
    
    print(f"✅ 装备页面生成完成，共 {len(items_data)} 件装备")

def generate_items_table(items_data):
    """生成装备表格HTML"""
    if not items_data:
        return '<div class="alert alert-warning">暂无装备数据</div>'
    
    table_html = '''
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">装备列表（前50件）</h5>
        </div>
        <div class="card-body">
            <table id="itemsTable" class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>名称</th>
                        <th>价格</th>
                        <th>攻击力</th>
                        <th>法强</th>
                        <th>生命值</th>
                        <th>护甲</th>
                        <th>魔抗</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for item in items_data:
        table_html += f'''
                    <tr>
                        <td><a href="/items/item_{items_data.index(item)+1}.html">{item.get('name', '未知')}</a></td>
                        <td><span class="badge bg-warning">{item.get('gold_total', 0)}</span></td>
                        <td>{item.get('ad', 0)}</td>
                        <td>{item.get('ap', 0)}</td>
                        <td>{item.get('health', 0)}</td>
                        <td>{item.get('armor', 0)}</td>
                        <td>{item.get('mr', 0)}</td>
                    </tr>
        '''
    
    table_html += '''
                </tbody>
            </table>
        </div>
    </div>
    '''
    
    return table_html

def generate_analysis_pages(docs_dir, project_dir):
    """生成比赛分析页面"""
    
    # 检查比赛数据
    match_stats = {
        'total_matches': 0,
        'avg_duration': '0:00',
        'modes': [],
        'patches': [],
        'ranks': []
    }
    
    db_path = project_dir / "instance" / "lol_data.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM matches")
            match_stats['total_matches'] = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT ROUND(AVG(game_duration_minutes), 1) FROM matches")
            avg_min = cursor.fetchone()[0] or 0
            match_stats['avg_duration'] = f"{int(avg_min)}:{int((avg_min % 1) * 60):02d}"
            
            cursor.execute("SELECT queue_type, COUNT(*) FROM matches GROUP BY queue_type LIMIT 5")
            match_stats['modes'] = cursor.fetchall()
            
            cursor.execute("SELECT patch_short, COUNT(*) FROM matches WHERE patch_short IS NOT NULL GROUP BY patch_short ORDER BY patch_short DESC LIMIT 5")
            match_stats['patches'] = cursor.fetchall()
            
            conn.close()
        except:
            pass
    
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>比赛分析 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container mt-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item active">比赛分析</li>
            </ol>
        </nav>
        
        <h1 class="mb-4"><i class="fas fa-chart-bar"></i> 比赛数据分析</h1>
        
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle"></i> 
            完整的数据分析功能（实时统计、图表生成、高级筛选）请访问
            <a href="https://mouxu.pythonanywhere.com/match_analysis" target="_blank" class="alert-link">PythonAnywhere动态版本</a>
        </div>
        
        <!-- 统计摘要 -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white bg-primary">
                    <div class="card-body text-center">
                        <h6>总比赛数</h6>
                        <h3>{match_stats['total_matches']}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-success">
                    <div class="card-body text-center">
                        <h6>平均时长</h6>
                        <h3>{match_stats['avg_duration']}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning">
                    <div class="card-body text-center">
                        <h6>游戏模式</h6>
                        <h3>{len(match_stats['modes'])}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-info">
                    <div class="card-body text-center">
                        <h6>游戏版本</h6>
                        <h3>{len(match_stats['patches'])}</h3>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 数据表格 -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">游戏模式分布</h5>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr><th>模式</th><th>比赛数</th></tr>
                            </thead>
                            <tbody>
                                {''.join([f'<tr><td>{mode[0]}</td><td>{mode[1]}</td></tr>' for mode in match_stats['modes']]) if match_stats['modes'] else '<tr><td colspan="2" class="text-center">暂无数据</td></tr>'}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">版本分布</h5>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr><th>版本</th><th>比赛数</th></tr>
                            </thead>
                            <tbody>
                                {''.join([f'<tr><td>{patch[0]}</td><td>{patch[1]}</td></tr>' for patch in match_stats['patches']]) if match_stats['patches'] else '<tr><td colspan="2" class="text-center">暂无数据</td></tr>'}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="card mt-4">
            <div class="card-header">
                <h5 class="mb-0">数据可视化</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <canvas id="modeChart" width="400" height="200"></canvas>
                    </div>
                    <div class="col-md-6">
                        <canvas id="patchChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-4">
            <a href="/" class="btn btn-outline-primary">
                <i class="fas fa-home"></i> 返回首页
            </a>
            <a href="/items/" class="btn btn-primary ms-2">
                <i class="fas fa-shield-alt"></i> 查看装备数据
            </a>
            <a href="https://mouxu.pythonanywhere.com/match_analysis" target="_blank" class="btn btn-success ms-2">
                <i class="fas fa-external-link-alt"></i> 完整数据分析
            </a>
        </div>
    </div>
    
    <script>
        // 图表数据
        const modeLabels = {json.dumps([mode[0] for mode in match_stats['modes']])};
        const modeData = {json.dumps([mode[1] for mode in match_stats['modes']])};
        
        const patchLabels = {json.dumps([patch[0] for patch in match_stats['patches']])};
        const patchData = {json.dumps([patch[1] for patch in match_stats['patches']])};
        
        // 初始化图表
        if (modeLabels.length > 0) {{
            new Chart(document.getElementById('modeChart').getContext('2d'), {{
                type: 'doughnut',
                data: {{
                    labels: modeLabels,
                    datasets: [{{
                        data: modeData,
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                        ]
                    }}]
                }}
            }});
        }}
        
        if (patchLabels.length > 0) {{
            new Chart(document.getElementById('patchChart').getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: patchLabels,
                    datasets: [{{
                        label: '比赛数量',
                        data: patchData,
                        backgroundColor: '#36A2EB'
                    }}]
                }}
            }});
        }}
    </script>
</body>
</html>
'''
    
    with open(docs_dir / "analysis" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 比赛分析页面生成完成")

def generate_data_files(docs_dir, project_dir):
    """生成数据文件页面和下载"""
    
    data_files = []
    
    # 检查CSV文件
    csv_files = ["ItemTbl.csv", "LOL_items_stats.csv", "MatchTbl.csv"]
    for csv_file in csv_files:
        csv_path = project_dir / csv_file
        if csv_path.exists():
            # 复制到docs/data目录
            import shutil
            shutil.copy2(csv_path, docs_dir / "data" / csv_file)
            data_files.append(csv_file)
    
    # 创建数据页面
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>数据下载 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item active">数据下载</li>
            </ol>
        </nav>
        
        <h1 class="mb-4"><i class="fas fa-database"></i> 数据文件下载</h1>
        
        <div class="alert alert-info">
            <h5><i class="fas fa-info-circle"></i> 数据说明</h5>
            <p class="mb-0">这里提供原始数据文件下载，可用于进一步分析或导入其他工具。</p>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">可用数据文件 ({len(data_files)}个)</h5>
            </div>
            <div class="card-body">
                {generate_data_table(data_files) if data_files else '<p class="text-center">暂无数据文件</p>'}
            </div>
        </div>
        
        <div class="mt-4">
            <a href="/" class="btn btn-outline-primary">
                <i class="fas fa-home"></i> 返回首页
            </a>
        </div>
    </div>
</body>
</html>
'''
    
    with open(docs_dir / "data" / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 数据文件页面生成完成，共 {len(data_files)} 个数据文件")

def generate_data_table(data_files):
    """生成数据文件表格"""
    table_html = '''
    <table class="table table-striped">
        <thead>
            <tr>
                <th>文件名</th>
                <th>大小</th>
                <th>描述</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    file_descriptions = {
        "ItemTbl.csv": "装备基本信息表",
        "LOL_items_stats.csv": "装备详细属性表", 
        "MatchTbl.csv": "比赛数据记录表"
    }
    
    for file in data_files:
        file_path = Path("/home/mouxu/project") / file
        size_kb = file_path.stat().st_size / 1024 if file_path.exists() else 0
        
        table_html += f'''
            <tr>
                <td><code>{file}</code></td>
                <td>{size_kb:.1f} KB</td>
                <td>{file_descriptions.get(file, '数据文件')}</td>
                <td>
                    <a href="/data/{file}" class="btn btn-sm btn-primary" download>
                        <i class="fas fa-download"></i> 下载
                    </a>
                </td>
            </tr>
        '''
    
    table_html += '''
        </tbody>
    </table>
    '''
    
    return table_html

def generate_about_page(docs_dir):
    """生成关于页面"""
    
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>关于项目 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item active">关于项目</li>
            </ol>
        </nav>
        
        <h1 class="mb-4"><i class="fas fa-info-circle"></i> 关于英雄联盟数据分析平台</h1>
        
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">项目简介</h5>
                <p class="card-text">
                    这是一个基于Flask和GitHub Pages的英雄联盟数据分析平台，采用双站协作架构，
                    结合了PythonAnywhere的动态处理能力和GitHub Pages的静态展示优势。
                </p>
                
                <h5 class="mt-4">技术架构</h5>
                <ul>
                    <li><strong>后端</strong>: Flask + SQLite + Pandas</li>
                    <li><strong>前端</strong>: Bootstrap 5 + Chart.js</li>
                    <li><strong>部署</strong>: PythonAnywhere + GitHub Pages</li>
                    <li><strong>自动化</strong>: Git + 定时同步脚本</li>
                </ul>
                
                <h5 class="mt-4">功能特点</h5>
                <div class="row">
                    <div class="col-md-6">
                        <ul>
                            <li>装备数据查询与分析</li>
                            <li>比赛数据统计与可视化</li>
                            <li>CSV文件上传与处理</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <ul>
                            <li>数据导出与分享</li>
                            <li>响应式网页设计</li>
                            <li>双站自动同步</li>
                        </ul>
                    </div>
                </div>
                
                <h5 class="mt-4">作者信息</h5>
                <p>GitHub: <a href="https://github.com/mouxu66">mouxu66</a></p>
                
                <div class="mt-4">
                    <a href="/" class="btn btn-primary">返回首页</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    with open(docs_dir / "about.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 关于页面生成完成")

if __name__ == "__main__":
    generate_complete_site()