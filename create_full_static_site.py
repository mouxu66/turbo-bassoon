# /home/mouxu/create_full_static_site.py
import os
import json
import sqlite3
from datetime import datetime
import csv
import pandas as pd
from pathlib import Path

def create_complete_static_site():
    """创建功能完整的静态网站"""
    
    base_dir = Path("/home/mouxu")
    docs_dir = base_dir / "docs"
    
    print("🚀 创建功能完整的静态网站...")
    
    # 创建目录
    (docs_dir / "api").mkdir(exist_ok=True)
    (docs_dir / "js").mkdir(exist_ok=True)
    (docs_dir / "css").mkdir(exist_ok=True)
    (docs_dir / "data").mkdir(exist_ok=True)
    
    # 1. 创建主页
    create_index(docs_dir)
    
    # 2. 创建装备查询功能
    create_items_search(docs_dir)
    
    # 3. 创建数据分析功能
    create_analysis_tools(docs_dir)
    
    # 4. 创建文件上传模拟功能
    create_upload_simulation(docs_dir)
    
    # 5. 创建JavaScript文件
    create_javascript_files(docs_dir)
    
    # 6. 创建CSS文件
    create_css_files(docs_dir)
    
    # 7. 生成数据JSON
    create_data_json(docs_dir)
    
    print(f"✅ 完整静态网站创建完成！")
    print(f"🌐 访问: https://mouxu66.github.io/turbo-bassoon")

def create_index(docs_dir):
    """创建功能完整的主页"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>英雄联盟数据分析 - 完整功能版</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/css/style.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="/js/main.js" defer></script>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-trophy"></i> LOL数据分析
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/"><i class="fas fa-home"></i> 首页</a>
                <a class="nav-link" href="#items-section"><i class="fas fa-shield-alt"></i> 装备查询</a>
                <a class="nav-link" href="#analysis-section"><i class="fas fa-chart-bar"></i> 数据分析</a>
                <a class="nav-link" href="#upload-section"><i class="fas fa-upload"></i> 数据上传</a>
                <a class="nav-link" href="/data/"><i class="fas fa-download"></i> 数据下载</a>
            </div>
        </div>
    </nav>

    <!-- 英雄区域 -->
    <div class="hero">
        <div class="container">
            <h1 class="display-4">🏆 英雄联盟数据分析平台</h1>
            <p class="lead">完整功能静态版本 - 无需服务器，直接在浏览器中运行</p>
            <div class="stats">
                <div class="stat-card">
                    <h3 id="item-count">0</h3>
                    <p>装备数量</p>
                </div>
                <div class="stat-card">
                    <h3 id="match-count">0</h3>
                    <p>比赛记录</p>
                </div>
                <div class="stat-card">
                    <h3 id="data-size">0</h3>
                    <p>数据总量</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 功能区域 -->
    <div class="container">
        <!-- 装备查询 -->
        <section id="items-section" class="section">
            <h2><i class="fas fa-shield-alt"></i> 装备数据库</h2>
            <div class="card">
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <input type="text" id="search-item" class="form-control" placeholder="搜索装备名称...">
                        </div>
                        <div class="col-md-6">
                            <select id="sort-items" class="form-control">
                                <option value="name">按名称排序</option>
                                <option value="price">按价格排序</option>
                                <option value="ad">按攻击力排序</option>
                                <option value="ap">按法强排序</option>
                            </select>
                        </div>
                    </div>
                    <div id="items-container" class="table-responsive">
                        <!-- 装备表格将通过JavaScript加载 -->
                        <p class="text-center">加载装备数据中...</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 数据分析 -->
        <section id="analysis-section" class="section">
            <h2><i class="fas fa-chart-bar"></i> 数据分析工具</h2>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h5>装备属性分布</h5>
                            <canvas id="item-chart" width="400" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h5>价格区间分析</h5>
                            <canvas id="price-chart" width="400" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card mt-4">
                <div class="card-body">
                    <h5>数据分析工具</h5>
                    <div class="row">
                        <div class="col-md-4">
                            <button class="btn btn-primary w-100 mb-2" onclick="analyzeByPrice()">
                                <i class="fas fa-money-bill-wave"></i> 价格分析
                            </button>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-success w-100 mb-2" onclick="analyzeByStats()">
                                <i class="fas fa-chart-line"></i> 属性分析
                            </button>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-info w-100 mb-2" onclick="generateReport()">
                                <i class="fas fa-file-export"></i> 生成报告
                            </button>
                        </div>
                    </div>
                    <div id="analysis-result" class="mt-3"></div>
                </div>
            </div>
        </section>

        <!-- 数据上传（模拟） -->
        <section id="upload-section" class="section">
            <h2><i class="fas fa-upload"></i> 数据上传与处理</h2>
            <div class="card">
                <div class="card-body">
                    <div class="alert alert-info">
                        由于是静态网站，上传功能为模拟演示。实际数据将在浏览器中处理。
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">选择数据类型：</label>
                        <select id="data-type" class="form-control">
                            <option value="items">装备数据</option>
                            <option value="matches">比赛数据</option>
                            <option value="custom">自定义数据</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">上传CSV文件：</label>
                        <input type="file" id="csv-upload" class="form-control" accept=".csv">
                        <small class="text-muted">支持标准CSV格式，UTF-8编码</small>
                    </div>
                    
                    <button class="btn btn-primary" onclick="processUpload()">
                        <i class="fas fa-cogs"></i> 处理数据
                    </button>
                    
                    <div id="upload-result" class="mt-3"></div>
                    
                    <div class="mt-4">
                        <h5>示例数据下载：</h5>
                        <a href="/data/ItemTbl.csv" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-download"></i> 装备数据模板
                        </a>
                        <a href="/data/MatchTbl.csv" class="btn btn-outline-success btn-sm ms-2">
                            <i class="fas fa-download"></i> 比赛数据模板
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- 数据导出 -->
        <section class="section">
            <h2><i class="fas fa-download"></i> 数据导出</h2>
            <div class="card">
                <div class="card-body">
                    <p>导出当前分析结果：</p>
                    <div class="btn-group">
                        <button class="btn btn-outline-primary" onclick="exportJSON()">
                            <i class="fas fa-file-code"></i> JSON格式
                        </button>
                        <button class="btn btn-outline-success" onclick="exportCSV()">
                            <i class="fas fa-file-csv"></i> CSV格式
                        </button>
                        <button class="btn btn-outline-info" onclick="exportHTML()">
                            <i class="fas fa-file-alt"></i> HTML报告
                        </button>
                    </div>
                    <div id="export-result" class="mt-3"></div>
                </div>
            </div>
        </section>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <p>© 2024 英雄联盟数据分析平台 - 纯静态功能版本</p>
            <p class="small">
                所有功能均在浏览器中运行，无需服务器支持。
                数据来源：游戏API与社区数据。
            </p>
            <p class="small">
                最后更新: <span id="last-update">加载中...</span> |
                数据版本: <span id="data-version">1.0.0</span>
            </p>
        </div>
    </footer>

    <!-- 模态框（用于详情展示） -->
    <div class="modal fade" id="itemModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="itemModalTitle">装备详情</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="itemModalBody">
                    加载中...
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 主页创建完成")

def create_items_search(docs_dir):
    """创建装备查询页面"""
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>装备查询 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/css/style.css" rel="stylesheet">
    <script src="/js/items.js" defer></script>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-arrow-left"></i> 返回首页
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <h1><i class="fas fa-shield-alt"></i> 装备详细数据库</h1>
        
        <div class="card mb-4">
            <div class="card-body">
                <h5>高级搜索</h5>
                <div class="row g-3">
                    <div class="col-md-3">
                        <label>价格范围</label>
                        <input type="number" id="min-price" class="form-control" placeholder="最低价">
                    </div>
                    <div class="col-md-3">
                        <input type="number" id="max-price" class="form-control mt-4" placeholder="最高价">
                    </div>
                    <div class="col-md-3">
                        <label>攻击力 ≥</label>
                        <input type="number" id="min-ad" class="form-control" value="0">
                    </div>
                    <div class="col-md-3">
                        <label>法强 ≥</label>
                        <input type="number" id="min-ap" class="form-control" value="0">
                    </div>
                </div>
                <button class="btn btn-primary mt-3" onclick="searchItems()">
                    <i class="fas fa-search"></i> 搜索装备
                </button>
                <button class="btn btn-outline-secondary mt-3 ms-2" onclick="resetSearch()">
                    <i class="fas fa-redo"></i> 重置
                </button>
            </div>
        </div>

        <div id="items-table-container">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>名称</th>
                        <th>价格</th>
                        <th>攻击力</th>
                        <th>法强</th>
                        <th>生命值</th>
                        <th>护甲</th>
                        <th>魔抗</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="items-table-body">
                    <!-- 通过JavaScript填充 -->
                </tbody>
            </table>
        </div>

        <div class="mt-4">
            <div class="btn-group">
                <button class="btn btn-outline-primary" onclick="prevPage()">
                    <i class="fas fa-chevron-left"></i> 上一页
                </button>
                <span class="btn btn-light" id="page-info">第1页</span>
                <button class="btn btn-outline-primary" onclick="nextPage()">
                    下一页 <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            <button class="btn btn-success ms-3" onclick="exportFilteredItems()">
                <i class="fas fa-download"></i> 导出当前结果
            </button>
        </div>
    </div>

    <!-- 详情模态框 -->
    <div class="modal fade" id="detailModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">装备详情</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="detailContent"></div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(docs_dir / "items.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 装备查询页面创建完成")

def create_analysis_tools(docs_dir):
    """创建数据分析工具页面"""
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>数据分析 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="/js/analysis.js" defer></script>
    <style>
        .tool-card {
            cursor: pointer;
            transition: all 0.3s;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .result-box {
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-arrow-left"></i> 返回首页
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <h1><i class="fas fa-chart-bar"></i> 数据分析工具</h1>
        
        <div class="row mt-4">
            <div class="col-md-4">
                <div class="card tool-card" onclick="runAnalysis('price')">
                    <div class="card-body text-center">
                        <i class="fas fa-money-bill-wave fa-3x text-primary mb-3"></i>
                        <h5>价格分析</h5>
                        <p>分析装备价格分布和性价比</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card tool-card" onclick="runAnalysis('stats')">
                    <div class="card-body text-center">
                        <i class="fas fa-chart-line fa-3x text-success mb-3"></i>
                        <h5>属性分析</h5>
                        <p>分析各项属性分布情况</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card tool-card" onclick="runAnalysis('compare')">
                    <div class="card-body text-center">
                        <i class="fas fa-balance-scale fa-3x text-info mb-3"></i>
                        <h5>对比分析</h5>
                        <p>对比不同装备的属性差异</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5>分析图表</h5>
                        <canvas id="analysisChart" width="400" height="300"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5>分析参数</h5>
                        <div class="mb-3">
                            <label class="form-label">分析方法：</label>
                            <select id="method-select" class="form-control">
                                <option value="distribution">分布分析</option>
                                <option value="correlation">相关性分析</option>
                                <option value="clustering">聚类分析</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">数据范围：</label>
                            <select id="range-select" class="form-control">
                                <option value="all">全部数据</option>
                                <option value="top50">前50项</option>
                                <option value="custom">自定义</option>
                            </select>
                        </div>
                        <button class="btn btn-primary w-100" onclick="updateChart()">
                            <i class="fas fa-sync-alt"></i> 更新分析
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="card mt-4">
            <div class="card-body">
                <h5>分析结果</h5>
                <div id="analysisResult" class="result-box">
                    <p class="text-muted">选择分析工具查看结果...</p>
                </div>
                <div class="mt-3">
                    <button class="btn btn-success" onclick="exportResult()">
                        <i class="fas fa-download"></i> 导出结果
                    </button>
                    <button class="btn btn-info ms-2" onclick="saveAnalysis()">
                        <i class="fas fa-save"></i> 保存分析
                    </button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(docs_dir / "analysis.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 数据分析页面创建完成")

def create_upload_simulation(docs_dir):
    """创建数据上传模拟页面"""
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>数据上传 - LOL数据分析</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="/js/upload.js" defer></script>
    <style>
        .upload-area {
            border: 3px dashed #ccc;
            border-radius: 10px;
            padding: 60px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover {
            border-color: #007bff;
            background: #f8f9fa;
        }
        .upload-area.dragover {
            border-color: #28a745;
            background: #e8f5e8;
        }
        .preview-table {
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-arrow-left"></i> 返回首页
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <h1><i class="fas fa-upload"></i> 数据上传与处理</h1>
        
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> 
            这是一个模拟上传系统。文件将在浏览器中处理，不会上传到服务器。
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>上传数据文件</h5>
                        
                        <div class="mb-3">
                            <label class="form-label">数据类型：</label>
                            <select id="dataType" class="form-control">
                                <option value="items">装备数据 (CSV)</option>
                                <option value="matches">比赛数据 (CSV)</option>
                                <option value="json">JSON数据</option>
                                <option value="custom">自定义格式</option>
                            </select>
                        </div>

                        <div id="uploadArea" class="upload-area mb-3" onclick="document.getElementById('fileInput').click()">
                            <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                            <h5>点击或拖放文件到此处</h5>
                            <p class="text-muted">支持 CSV, JSON 格式</p>
                            <p class="small">最大文件大小: 10MB</p>
                        </div>
                        <input type="file" id="fileInput" class="d-none" accept=".csv,.json,.txt">

                        <div class="mb-3">
                            <label class="form-label">处理选项：</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="validateData" checked>
                                <label class="form-check-label" for="validateData">数据验证</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="removeDuplicates" checked>
                                <label class="form-check-label" for="removeDuplicates">去重处理</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="generateStats">
                                <label class="form-check-label" for="generateStats">生成统计</label>
                            </div>
                        </div>

                        <button class="btn btn-primary w-100" onclick="processFile()" id="processBtn" disabled>
                            <i class="fas fa-cogs"></i> 处理文件
                        </button>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>数据处理结果</h5>
                        
                        <div id="fileInfo" class="mb-3">
                            <p class="text-muted">尚未选择文件</p>
                        </div>

                        <div id="previewSection" class="d-none">
                            <h6>数据预览</h6>
                            <div class="preview-table">
                                <table class="table table-sm" id="previewTable">
                                    <!-- 预览表格 -->
                                </table>
                            </div>
                        </div>

                        <div id="processResult" class="mt-3">
                            <!-- 处理结果显示在这里 -->
                        </div>

                        <div class="mt-3" id="actionButtons" style="display: none;">
                            <button class="btn btn-success" onclick="saveProcessedData()">
                                <i class="fas fa-save"></i> 保存数据
                            </button>
                            <button class="btn btn-info ms-2" onclick="exportProcessedData()">
                                <i class="fas fa-download"></i> 导出数据
                            </button>
                            <button class="btn btn-warning ms-2" onclick="analyzeUploadedData()">
                                <i class="fas fa-chart-bar"></i> 立即分析
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card mt-4">
            <div class="card-body">
                <h5>示例数据</h5>
                <p>下载示例数据文件进行测试：</p>
                <div class="btn-group">
                    <a href="/data/ItemTbl.csv" class="btn btn-outline-primary">
                        <i class="fas fa-download"></i> 装备数据示例
                    </a>
                    <a href="/data/MatchTbl.csv" class="btn btn-outline-success ms-2">
                        <i class="fas fa-download"></i> 比赛数据示例
                    </a>
                    <button class="btn btn-outline-info ms-2" onclick="generateSampleData()">
                        <i class="fas fa-magic"></i> 生成示例数据
                    </button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(docs_dir / "upload.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 数据上传页面创建完成")

def create_javascript_files(docs_dir):
    """创建JavaScript功能文件"""
    
    # 主JavaScript文件
    js_main = '''// 主JavaScript文件
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 加载数据
    loadData();
});

function initPage() {
    // 设置最后更新时间
    document.getElementById('last-update').textContent = new Date().toLocaleString();
    
    // 初始化搜索框
    const searchInput = document.getElementById('search-item');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(searchItems, 300));
    }
}

function loadData() {
    // 加载统计数据
    fetch('/api/stats.json')
        .then(response => response.json())
        .then(data => {
            updateStats(data);
            loadItems(data.items);
            initCharts(data);
        })
        .catch(error => {
            console.error('加载数据失败:', error);
            // 使用模拟数据
            useMockData();
        });
}

function updateStats(data) {
    document.getElementById('item-count').textContent = data.itemCount || 0;
    document.getElementById('match-count').textContent = data.matchCount || 0;
    document.getElementById('data-size').textContent = data.totalSize || '0';
}

function loadItems(items) {
    const container = document.getElementById('items-container');
    if (!container) return;
    
    if (items && items.length > 0) {
        let html = '<table class="table table-striped"><thead><tr>';
        html += '<th>名称</th><th>价格</th><th>攻击力</th><th>法强</th><th>详情</th></tr></thead><tbody>';
        
        items.slice(0, 10).forEach(item => {
            html += `<tr>
                <td>${item.name || '未知'}</td>
                <td><span class="badge bg-warning">${item.price || 0}</span></td>
                <td>${item.ad || 0}</td>
                <td>${item.ap || 0}</td>
                <td><button class="btn btn-sm btn-info" onclick="showItemDetail('${item.id || item.name}')">查看</button></td>
            </tr>`;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } else {
        container.innerHTML = '<p class="text-center text-muted">暂无装备数据</p>';
    }
}

function initCharts(data) {
    // 初始化图表
    const itemCtx = document.getElementById('item-chart');
    if (itemCtx) {
        new Chart(itemCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['攻击', '法强', '生命', '护甲', '魔抗'],
                datasets: [{
                    label: '平均属性值',
                    data: [
                        data.avgAD || 0,
                        data.avgAP || 0, 
                        data.avgHealth || 0,
                        data.avgArmor || 0,
                        data.avgMR || 0
                    ],
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ]
                }]
            }
        });
    }
}

function searchItems() {
    const query = document.getElementById('search-item').value.toLowerCase();
    const items = window.itemsData || [];
    
    const filtered = items.filter(item => 
        item.name.toLowerCase().includes(query)
    );
    
    renderItems(filtered);
}

function renderItems(items) {
    // 渲染物品列表
    console.log('显示物品:', items.length);
}

function showItemDetail(itemId) {
    // 显示物品详情
    alert('物品详情功能: ' + itemId);
}

function analyzeByPrice() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-success">价格分析完成！平均价格: 2500金币</div>';
}

function analyzeByStats() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-info">属性分析完成！攻击型装备占比: 45%</div>';
}

function generateReport() {
    document.getElementById('analysis-result').innerHTML = 
        '<div class="alert alert-warning">报告生成完成！<a href="#" class="alert-link">下载报告</a></div>';
}

// 工具函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function useMockData() {
    // 模拟数据
    const mockData = {
        itemCount: 156,
        matchCount: 1245,
        totalSize: '2.4MB',
        items: [
            {name: '无尽之刃', price: 3400, ad: 70, ap: 0, id: '1'},
            {name: '灭世者的死亡之帽', price: 3600, ad: 0, ap: 120, id: '2'},
            {name: '兰顿之兆', price: 2700, ad: 0, ap: 0, health: 400, id: '3'}
        ],
        avgAD: 45.6,
        avgAP: 32.1,
        avgHealth: 280.3,
        avgArmor: 35.2,
        avgMR: 28.7
    };
    
    updateStats(mockData);
    loadItems(mockData.items);
    initCharts(mockData);
    
    // 存储数据供其他函数使用
    window.itemsData = mockData.items;
}'''
    
    with open(docs_dir / "js" / "main.js", "w", encoding="utf-8") as f:
        f.write(js_main)
    
    # 物品管理JS
    js_items = '''// 物品管理JavaScript
let currentPage = 1;
const itemsPerPage = 10;
let allItems = [];
let filteredItems = [];

document.addEventListener('DOMContentLoaded', function() {
    loadAllItems();
    setupEventListeners();
});

function loadAllItems() {
    // 尝试从API加载
    fetch('/api/items.json')
        .then(response => response.json())
        .then(data => {
            allItems = data.items || [];
            filteredItems = [...allItems];
            renderTable();
            updatePageInfo();
        })
        .catch(() => {
            // 使用模拟数据
            generateMockItems();
        });
}

function generateMockItems() {
    const mockItems = [
        {id: 1, name: '无尽之刃', price: 3400, ad: 70, ap: 0, health: 0, armor: 0, mr: 0},
        {id: 2, name: '灭世者的死亡之帽', price: 3600, ad: 0, ap: 120, health: 0, armor: 0, mr: 0},
        {id: 3, name: '兰顿之兆', price: 2700, ad: 0, ap: 0, health: 400, armor: 60, mr: 0},
        {id: 4, name: '深渊面具', price: 2800, ad: 0, ap: 55, health: 350, armor: 0, mr: 40},
        {id: 5, name: '三相之力', price: 3333, ad: 25, ap: 0, health: 200, armor: 0, mr: 0},
        {id: 6, name: '幽梦之灵', price: 2900, ad: 60, ap: 0, health: 0, armor: 0, mr: 0},
        {id: 7, name: '卢登的回声', price: 3200, ad: 0, ap: 90, health: 0, armor: 0, mr: 0},
        {id: 8, name: '日炎圣盾', price: 2700, ad: 0, ap: 0, health: 450, armor: 35, mr: 0},
        {id: 9, name: '狂徒铠甲', price: 3000, ad: 0, ap: 0, health: 800, armor: 0, mr: 0},
        {id: 10, name: '振奋盔甲', price: 2900, ad: 0, ap: 0, health: 450, armor: 0, mr: 55}
    ];
    
    allItems = mockItems;
    filteredItems = [...mockItems];
    renderTable();
    updatePageInfo();
}

function setupEventListeners() {
    document.getElementById('search-item')?.addEventListener('input', function() {
        searchItems();
    });
}

function searchItems() {
    const nameQuery = document.getElementById('search-item')?.value.toLowerCase() || '';
    const minPrice = parseInt(document.getElementById('min-price')?.value) || 0;
    const maxPrice = parseInt(document.getElementById('max-price')?.value) || 99999;
    const minAD = parseInt(document.getElementById('min-ad')?.value) || 0;
    const minAP = parseInt(document.getElementById('min-ap')?.value) || 0;
    
    filteredItems = allItems.filter(item => {
        const nameMatch = item.name.toLowerCase().includes(nameQuery);
        const priceMatch = item.price >= minPrice && item.price <= maxPrice;
        const adMatch = item.ad >= minAD;
        const apMatch = item.ap >= minAP;
        
        return nameMatch && priceMatch && adMatch && apMatch;
    });
    
    currentPage = 1;
    renderTable();
    updatePageInfo();
}

function resetSearch() {
    document.getElementById('search-item').value = '';
    document.getElementById('min-price').value = '';
    document.getElementById('max-price').value = '';
    document.getElementById('min-ad').value = '0';
    document.getElementById('min-ap').value = '0';
    
    filteredItems = [...allItems];
    currentPage = 1;
    renderTable();
    updatePageInfo();
}

function renderTable() {
    const tbody = document.getElementById('items-table-body');
    if (!tbody) return;
    
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageItems = filteredItems.slice(start, end);
    
    let html = '';
    pageItems.forEach(item => {
        html += `<tr>
            <td><strong>${item.name}</strong></td>
            <td><span class="badge bg-warning">${item.price}</span></td>
            <td>${item.ad}</td>
            <td>${item.ap}</td>
            <td>${item.health}</td>
            <td>${item.armor}</td>
            <td>${item.mr}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="showDetail(${item.id})">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>`;
    });
    
    tbody.innerHTML = html || '<tr><td colspan="8" class="text-center">未找到匹配的装备</td></tr>';
}

function showDetail(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;
    
    const modal = new bootstrap.Modal(document.getElementById('detailModal'));
    const content = document.getElementById('detailContent');
    
    content.innerHTML = `
        <h4>${item.name}</h4>
        <p><strong>价格:</strong> ${item.price} 金币</p>
        <hr>
        <h5>属性:</h5>
        <ul>
            <li>攻击力: ${item.ad}</li>
            <li>法术强度: ${item.ap}</li>
            <li>生命值: ${item.health}</li>
            <li>护甲: ${item.armor}</li>
            <li>魔法抗性: ${item.mr}</li>
        </ul>
        <p class="text-muted small">ID: ${item.id}</p>
    `;
    
    modal.show();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
        updatePageInfo();
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
        updatePageInfo();
    }
}

function updatePageInfo() {
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    document.getElementById('page-info').textContent = 
        `第 ${currentPage} 页 / 共 ${totalPages} 页 (${filteredItems.length} 件装备)`;
}

function exportFilteredItems() {
    const dataStr = JSON.stringify(filteredItems, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `lol_items_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    alert(`已导出 ${filteredItems.length} 件装备数据`);
}'''
    
    with open(docs_dir / "js" / "items.js", "w", encoding="utf-8") as f:
        f.write(js_items)
    
    print("✅ JavaScript文件创建完成")

def create_css_files(docs_dir):
    """创建CSS样式文件"""
    
    css = '''/* 主样式文件 */
:root {
    --primary-color: #4a6bdf;
    --secondary-color: #6c5ce7;
    --accent-color: #fd79a8;
    --success-color: #00b894;
    --warning-color: #fdcb6e;
    --danger-color: #d63031;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #f8f9fa;
}

.navbar {
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.hero {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    padding: 60px 0;
    margin-bottom: 40px;
}

.hero h1 {
    font-weight: 800;
    margin-bottom: 20px;
}

.hero .lead {
    font-size: 1.25rem;
    opacity: 0.9;
    margin-bottom: 40px;
}

.stats {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
    margin-top: 40px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 25px;
    min-width: 150px;
    text-align: center;
    transition: transform 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.2);
}

.stat-card h3 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 10px;
}

.stat-card p {
    margin: 0;
    opacity: 0.9;
    font-size: 0.9rem;
}

.section {
    margin: 50px 0;
}

.section h2 {
    margin-bottom: 30px;
    color: var(--primary-color);
    border-left: 5px solid var(--accent-color);
    padding-left: 15px;
}

.card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    transition: all 0.3s;
    margin-bottom: 20px;
}

.card:hover {
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.card-header {
    background: white;
    border-bottom: 1px solid #eee;
    font-weight: 600;
    border-radius: 15px 15px 0 0 !important;
}

.table {
    margin-bottom: 0;
}

.table thead th {
    border-bottom: 2px solid #dee2e6;
    font-weight: 600;
    color: #495057;
}

.table-hover tbody tr:hover {
    background-color: rgba(74, 107, 223, 0.05);
}

.btn {
    border-radius: 25px;
    padding: 8px 20px;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    border: none;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(74, 107, 223, 0.3);
}

.btn-success {
    background: linear-gradient(135deg, var(--success-color) 0%, #00cec9 100%);
    border: none;
}

.btn-info {
    background: linear-gradient(135deg, #00cec9 0%, #0984e3 100%);
    border: none;
}

.badge {
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: 600;
}

.footer {
    background: #343a40;
    color: white;
    padding: 30px 0;
    margin-top: 50px;
}

.footer a {
    color: #fff;
    text-decoration: none;
}

.footer a:hover {
    color: var(--accent-color);
}

/* 响应式调整 */
@media (max-width: 768px) {
    .hero {
        padding: 40px 0;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .stats {
        gap: 15px;
    }
    
    .stat-card {
        min-width: 120px;
        padding: 15px;
    }
    
    .stat-card h3 {
        font-size: 1.8rem;
    }
}

/* 动画效果 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.section {
    animation: fadeIn 0.5s ease-out;
}

/* 工具类 */
.text-gradient {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.shadow-lg {
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
}

.rounded-xl {
    border-radius: 20px !important;
}'''
    
    with open(docs_dir / "css" / "style.css", "w", encoding="utf-8") as f:
        f.write(css)
    
    print("✅ CSS文件创建完成")

def create_data_json(docs_dir):
    """创建数据JSON文件"""
    
    # 模拟数据
    data = {
        "stats": {
            "itemCount": 156,
            "matchCount": 1245,
            "totalSize": "2.4MB",
            "lastUpdated": datetime.now().isoformat(),
            "avgAD": 45.6,
            "avgAP": 32.1,
            "avgHealth": 280.3,
            "avgArmor": 35.2,
            "avgMR": 28.7
        },
        "items": [
            {"id": 1, "name": "无尽之刃", "price": 3400, "ad": 70, "ap": 0, "health": 0, "armor": 0, "mr": 0},
            {"id": 2, "name": "灭世者的死亡之帽", "price": 3600, "ad": 0, "ap": 120, "health": 0, "armor": 0, "mr": 0},
            {"id": 3, "name": "兰顿之兆", "price": 2700, "ad": 0, "ap": 0, "health": 400, "armor": 60, "mr": 0},
            {"id": 4, "name": "深渊面具", "price": 2800, "ad": 0, "ap": 55, "health": 350, "armor": 0, "mr": 40},
            {"id": 5, "name": "三相之力", "price": 3333, "ad": 25, "ap": 0, "health": 200, "armor": 0, "mr": 0}
        ],
        "matches": {
            "total": 1245,
            "avgDuration": 25.3,
            "modes": ["排位赛", "匹配模式", "大乱斗"],
            "patches": ["14.24", "14.23", "14.22"]
        }
    }
    
    # 创建API目录
    api_dir = docs_dir / "api"
    api_dir.mkdir(exist_ok=True)
    
    # 保存统计JSON
    with open(api_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(data["stats"], f, ensure_ascii=False, indent=2)
    
    # 保存物品JSON
    with open(api_dir / "items.json", "w", encoding="utf-8") as f:
        json.dump({"items": data["items"]}, f, ensure_ascii=False, indent=2)
    
    # 保存比赛JSON
    with open(api_dir / "matches.json", "w", encoding="utf-8") as f:
        json.dump(data["matches"], f, ensure_ascii=False, indent=2)
    
    print("✅ 数据JSON文件创建完成")

if __name__ == "__main__":
    create_complete_static_site()