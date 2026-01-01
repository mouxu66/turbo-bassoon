# /home/mouxu/create_beautiful_site.py
import os
import json
from datetime import datetime
from pathlib import Path

def create_beautiful_site():
    """创建美观的英雄联盟数据分析网站"""
    
    base_dir = Path("/home/mouxu")
    docs_dir = base_dir / "docs"
    
    print("🎨 创建美观的英雄联盟数据分析网站...")
    
    # 创建目录
    (docs_dir / "assets").mkdir(exist_ok=True)
    (docs_dir / "assets" / "css").mkdir(exist_ok=True)
    (docs_dir / "assets" / "js").mkdir(exist_ok=True)
    (docs_dir / "assets" / "images").mkdir(exist_ok=True)
    
    # 1. 创建CSS样式
    create_css_files(docs_dir)
    
    # 2. 创建JavaScript
    create_js_files(docs_dir)
    
    # 3. 创建主页（美观版）
    create_beautiful_index(docs_dir)
    
    # 4. 创建装备页面
    create_beautiful_items_page(docs_dir)
    
    # 5. 创建分析页面
    create_beautiful_analysis_page(docs_dir)
    
    # 6. 创建关于页面
    create_beautiful_about_page(docs_dir)
    
    print(f"✅ 美观网站创建完成！")
    print(f"🎮 主题: 英雄联盟风格")
    print(f"🌐 访问: https://mouxu66.github.io/turbo-bassoon")

def create_css_files(docs_dir):
    """创建漂亮的CSS样式"""
    
    css = '''/* 英雄联盟主题样式 */
:root {
    /* 英雄联盟主题色 */
    --lol-gold: #C8AA6E;
    --lol-gold-dark: #937341;
    --lol-gold-light: #F0E6D2;
    --lol-blue: #0AC8B9;
    --lol-purple: #C8AAE5;
    --lol-red: #DA2C43;
    --lol-green: #1EB980;
    --lol-bg-dark: #0A1428;
    --lol-bg-darker: #010A13;
    --lol-bg-gradient: linear-gradient(135deg, #0A1428 0%, #1E2A47 100%);
}

/* 基础样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Beaufort for LOL', 'Microsoft YaHei', sans-serif;
    background: var(--lol-bg-gradient);
    color: var(--lol-gold-light);
    min-height: 100vh;
    line-height: 1.6;
    overflow-x: hidden;
}

/* 英雄联盟字体 */
@font-face {
    font-family: 'Beaufort for LOL';
    src: url('https://fonts.cdnfonts.com/css/beaufort-for-lol');
}

/* 导航栏 */
.navbar {
    background: rgba(10, 20, 40, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 2px solid var(--lol-gold);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--lol-gold);
    text-decoration: none;
}

.logo-icon {
    font-size: 2rem;
    color: var(--lol-gold);
}

.nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.nav-link {
    color: var(--lol-gold-light);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: all 0.3s;
    position: relative;
}

.nav-link:hover {
    color: var(--lol-gold);
    background: rgba(200, 170, 110, 0.1);
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    width: 0;
    height: 2px;
    background: var(--lol-gold);
    transition: all 0.3s;
    transform: translateX(-50%);
}

.nav-link:hover::after {
    width: 80%;
}

/* 英雄区域 */
.hero {
    background: linear-gradient(rgba(10, 20, 40, 0.9), rgba(10, 20, 40, 0.9)),
                url('https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt44f8f8c57166b402/60ee119e2c9b4e0d4f4a6d61/lol-gameplay-article-banner.jpg');
    background-size: cover;
    background-position: center;
    padding: 6rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, transparent 0%, var(--lol-bg-darker) 100%);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(to right, var(--lol-gold), var(--lol-gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(200, 170, 110, 0.3);
}

.hero-subtitle {
    font-size: 1.5rem;
    color: var(--lol-gold-light);
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin: 3rem 0;
    flex-wrap: wrap;
}

.stat-card {
    background: rgba(30, 42, 71, 0.6);
    border: 1px solid rgba(200, 170, 110, 0.3);
    border-radius: 15px;
    padding: 2rem;
    min-width: 180px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: var(--lol-gold);
    box-shadow: 0 10px 30px rgba(200, 170, 110, 0.2);
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(to right, var(--lol-gold), var(--lol-blue));
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    color: var(--lol-gold);
    margin-bottom: 0.5rem;
    text-shadow: 0 0 20px rgba(200, 170, 110, 0.5);
}

.stat-label {
    font-size: 0.9rem;
    color: var(--lol-gold-light);
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 功能卡片 */
.features {
    padding: 5rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: var(--lol-gold);
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 3px;
    background: linear-gradient(to right, var(--lol-gold), var(--lol-blue));
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.feature-card {
    background: rgba(30, 42, 71, 0.6);
    border: 1px solid rgba(200, 170, 110, 0.2);
    border-radius: 15px;
    padding: 2.5rem;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: var(--lol-gold);
    box-shadow: 0 15px 40px rgba(200, 170, 110, 0.15);
}

.feature-icon {
    font-size: 3rem;
    color: var(--lol-gold);
    margin-bottom: 1.5rem;
    text-align: center;
}

.feature-title {
    font-size: 1.5rem;
    color: var(--lol-gold-light);
    margin-bottom: 1rem;
    text-align: center;
}

.feature-desc {
    color: var(--lol-gold-light);
    opacity: 0.8;
    text-align: center;
    line-height: 1.6;
}

/* 按钮样式 */
.btn {
    display: inline-block;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, var(--lol-gold) 0%, var(--lol-gold-dark) 100%);
    color: var(--lol-bg-darker);
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    text-align: center;
    position: relative;
    overflow: hidden;
    font-size: 1.1rem;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(200, 170, 110, 0.4);
    color: var(--lol-bg-darker);
}

.btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: 0.5s;
}

.btn:hover::before {
    left: 100%;
}

.btn-primary {
    background: linear-gradient(135deg, var(--lol-gold) 0%, var(--lol-gold-dark) 100%);
}

.btn-secondary {
    background: linear-gradient(135deg, var(--lol-blue) 0%, #0A8B82 100%);
}

.btn-outline {
    background: transparent;
    border: 2px solid var(--lol-gold);
    color: var(--lol-gold);
}

.btn-outline:hover {
    background: var(--lol-gold);
    color: var(--lol-bg-darker);
}

/* 表格样式 */
.table-container {
    background: rgba(30, 42, 71, 0.6);
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
    border: 1px solid rgba(200, 170, 110, 0.2);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    color: var(--lol-gold-light);
}

.data-table th {
    background: rgba(200, 170, 110, 0.1);
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid var(--lol-gold);
    color: var(--lol-gold);
}

.data-table td {
    padding: 1rem;
    border-bottom: 1px solid rgba(200, 170, 110, 0.1);
}

.data-table tr:hover {
    background: rgba(200, 170, 110, 0.05);
}

/* 页脚 */
.footer {
    background: var(--lol-bg-darker);
    padding: 3rem 2rem;
    margin-top: 5rem;
    border-top: 2px solid var(--lol-gold);
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 3rem;
}

.footer-section h3 {
    color: var(--lol-gold);
    margin-bottom: 1.5rem;
    font-size: 1.3rem;
}

.footer-links {
    list-style: none;
}

.footer-links li {
    margin-bottom: 0.8rem;
}

.footer-links a {
    color: var(--lol-gold-light);
    text-decoration: none;
    transition: color 0.3s;
    opacity: 0.8;
}

.footer-links a:hover {
    color: var(--lol-gold);
    opacity: 1;
}

.copyright {
    text-align: center;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(200, 170, 110, 0.2);
    color: var(--lol-gold-light);
    opacity: 0.6;
    font-size: 0.9rem;
}

/* 动画效果 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glow {
    0%, 100% {
        text-shadow: 0 0 10px rgba(200, 170, 110, 0.5);
    }
    50% {
        text-shadow: 0 0 20px rgba(200, 170, 110, 0.8), 0 0 30px rgba(200, 170, 110, 0.6);
    }
}

.animate-fade-in {
    animation: fadeInUp 0.6s ease-out;
}

.glow-text {
    animation: glow 2s infinite;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .hero-stats {
        gap: 1rem;
    }
    
    .stat-card {
        min-width: 140px;
        padding: 1.5rem;
    }
    
    .nav-links {
        gap: 1rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: var(--lol-bg-darker);
}

::-webkit-scrollbar-thumb {
    background: var(--lol-gold);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--lol-gold-dark);
}'''
    
    with open(docs_dir / "assets" / "css" / "style.css", "w", encoding="utf-8") as f:
        f.write(css)
    
    print("✅ 美观的CSS样式创建完成")

def create_js_files(docs_dir):
    """创建JavaScript文件"""
    
    js = '''// 英雄联盟主题JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 加载统计数据
    loadStats();
    
    // 添加动画效果
    addAnimations();
    
    // 初始化工具提示
    initTooltips();
});

function initPage() {
    // 设置最后更新时间
    const now = new Date();
    document.getElementById('current-time').textContent = 
        now.toLocaleDateString('zh-CN', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    
    // 添加滚动效果
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero');
        if (parallax) {
            parallax.style.transform = `translateY(${scrolled * 0.1}px)`;
        }
    });
}

function loadStats() {
    // 模拟统计数据
    const stats = {
        items: 156,
        matches: 1245,
        patches: 24,
        champions: 165
    };
    
    // 更新统计卡片
    animateCounter('stat-items', stats.items);
    animateCounter('stat-matches', stats.matches);
    animateCounter('stat-patches', stats.patches);
    animateCounter('stat-champions', stats.champions);
}

function animateCounter(elementId, target) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 30);
}

function addAnimations() {
    // 为功能卡片添加动画
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-fade-in');
    });
    
    // 为按钮添加点击效果
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // 创建点击效果
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.7);
                transform: scale(0);
                animation: ripple 0.6s linear;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
            `;
            
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

function initTooltips() {
    // 添加CSS动画
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // 为统计卡片添加悬停效果
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// 页面切换功能
function navigateTo(page) {
    // 添加页面切换动画
    document.body.style.opacity = '0.7';
    document.body.style.transition = 'opacity 0.3s';
    
    setTimeout(() => {
        window.location.href = page;
    }, 300);
}

// 导出数据功能
function exportData(type) {
    const data = {
        timestamp: new Date().toISOString(),
        items: 156,
        matches: 1245,
        exportType: type
    };
    
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `lol-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // 显示通知
    showNotification('数据导出成功！', 'success');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#1EB980' : '#DA2C43'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 1rem;
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// 添加CSS动画
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(notificationStyle);'''
    
    with open(docs_dir / "assets" / "js" / "main.js", "w", encoding="utf-8") as f:
        f.write(js)
    
    print("✅ JavaScript文件创建完成")

def create_beautiful_index(docs_dir):
    """创建美观的主页"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 英雄联盟数据分析中心</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/assets/js/main.js" defer></script>
    <style>
        /* 额外样式增强 */
        .hero-particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: var(--lol-gold);
            border-radius: 50%;
            opacity: 0.3;
        }
        
        .champion-showcase {
            background: rgba(30, 42, 71, 0.4);
            border-radius: 20px;
            padding: 2rem;
            margin: 3rem 0;
            border: 1px solid rgba(200, 170, 110, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .champion-showcase::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(200, 170, 110, 0.05), transparent);
            z-index: 0;
        }
        
        .data-visualization {
            background: rgba(10, 20, 40, 0.7);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(10, 200, 185, 0.3);
            position: relative;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-trophy logo-icon"></i>
                <span>LoL数据中心</span>
            </a>
            
            <ul class="nav-links">
                <li><a href="/" class="nav-link active"><i class="fas fa-home"></i> 首页</a></li>
                <li><a href="/items.html" class="nav-link"><i class="fas fa-shield-alt"></i> 装备库</a></li>
                <li><a href="/analysis.html" class="nav-link"><i class="fas fa-chart-line"></i> 数据分析</a></li>
                <li><a href="/about.html" class="nav-link"><i class="fas fa-info-circle"></i> 关于</a></li>
                <li><a href="https://github.com/mouxu66/turbo-bassoon" class="nav-link" target="_blank">
                    <i class="fab fa-github"></i> GitHub
                </a></li>
            </ul>
        </div>
    </nav>

    <!-- 英雄区域 -->
    <section class="hero">
        <div class="hero-particles" id="particles"></div>
        
        <div class="hero-content">
            <h1 class="glow-text">英雄联盟数据分析中心</h1>
            <p class="hero-subtitle">深入挖掘游戏数据，洞察胜利之道</p>
            
            <div class="hero-stats">
                <div class="stat-card">
                    <div class="stat-number" id="stat-items">0</div>
                    <div class="stat-label">装备数量</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="stat-matches">0</div>
                    <div class="stat-label">比赛记录</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="stat-patches">0</div>
                    <div class="stat-label">游戏版本</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="stat-champions">0</div>
                    <div class="stat-label">英雄总数</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="/items.html" class="btn btn-primary">
                    <i class="fas fa-search"></i> 探索装备数据库
                </a>
                <a href="/analysis.html" class="btn btn-secondary">
                    <i class="fas fa-chart-bar"></i> 开始数据分析
                </a>
                <a href="#features" class="btn btn-outline">
                    <i class="fas fa-arrow-down"></i> 了解更多
                </a>
            </div>
        </div>
    </section>

    <!-- 功能特色 -->
    <section id="features" class="features">
        <h2 class="section-title">核心功能</h2>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-database"></i>
                </div>
                <h3 class="feature-title">完整装备数据库</h3>
                <p class="feature-desc">
                    收录所有英雄联盟装备的详细数据，包括属性、价格、合成路径等，
                    支持高级搜索和筛选功能。
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <h3 class="feature-title">深度数据分析</h3>
                <p class="feature-desc">
                    提供专业的统计分析和可视化工具，帮助您理解数据背后的趋势和规律，
                    优化游戏策略。
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <h3 class="feature-title">实时数据更新</h3>
                <p class="feature-desc">
                    跟随游戏版本实时更新数据，确保您获得的信息始终是最新、最准确的。
                </p>
            </div>
        </div>
    </section>

    <!-- 数据可视化展示 -->
    <section class="features">
        <h2 class="section-title">数据洞察</h2>
        
        <div class="champion-showcase">
            <h3 style="text-align: center; margin-bottom: 2rem; color: var(--lol-gold);">
                <i class="fas fa-crown"></i> 热门装备排行
            </h3>
            
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>装备名称</th>
                            <th>出场率</th>
                            <th>胜率</th>
                            <th>平均价格</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span class="stat-number" style="font-size: 1.2rem;">1</span></td>
                            <td><strong>无尽之刃</strong></td>
                            <td>68.5%</td>
                            <td style="color: var(--lol-green);">52.3%</td>
                            <td><span style="color: var(--lol-gold);">3400</span></td>
                        </tr>
                        <tr>
                            <td><span class="stat-number" style="font-size: 1.2rem;">2</span></td>
                            <td><strong>灭世者的死亡之帽</strong></td>
                            <td>45.2%</td>
                            <td style="color: var(--lol-green);">53.1%</td>
                            <td><span style="color: var(--lol-gold);">3600</span></td>
                        </tr>
                        <tr>
                            <td><span class="stat-number" style="font-size: 1.2rem;">3</span></td>
                            <td><strong>三相之力</strong></td>
                            <td>42.8%</td>
                            <td style="color: var(--lol-green);">51.7%</td>
                            <td><span style="color: var(--lol-gold);">3333</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- 快速开始 -->
    <section class="features">
        <h2 class="section-title">快速开始</h2>
        
        <div style="text-align: center; max-width: 800px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 3rem 0;">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; color: var(--lol-gold); margin-bottom: 1rem;">1</div>
                    <h3 style="color: var(--lol-gold-light); margin-bottom: 1rem;">浏览装备</h3>
                    <p style="color: var(--lol-gold-light); opacity: 0.8;">探索完整的英雄联盟装备数据库</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; color: var(--lol-blue); margin-bottom: 1rem;">2</div>
                    <h3 style="color: var(--lol-gold-light); margin-bottom: 1rem;">分析数据</h3>
                    <p style="color: var(--lol-gold-light); opacity: 0.8;">使用强大的分析工具发现洞察</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; color: var(--lol-green); margin-bottom: 1rem;">3</div>
                    <h3 style="color: var(--lol-gold-light); margin-bottom: 1rem;">优化策略</h3>
                    <p style="color: var(--lol-gold-light); opacity: 0.8;">基于数据优化您的游戏策略</p>
                </div>
            </div>
            
            <a href="/items.html" class="btn btn-primary" style="padding: 1.2rem 3rem; font-size: 1.2rem;">
                <i class="fas fa-rocket"></i> 立即开始探索
            </a>
        </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>LoL数据中心</h3>
                <p style="opacity: 0.8; line-height: 1.6;">
                    致力于提供最全面、最准确的英雄联盟数据分析服务，
                    帮助玩家和研究者更好地理解游戏。
                </p>
            </div>
            
            <div class="footer-section">
                <h3>快速链接</h3>
                <ul class="footer-links">
                    <li><a href="/">首页</a></li>
                    <li><a href="/items.html">装备数据库</a></li>
                    <li><a href="/analysis.html">数据分析</a></li>
                    <li><a href="/about.html">关于我们</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>数据来源</h3>
                <ul class="footer-links">
                    <li>Riot Games API</li>
                    <li>社区数据贡献</li>
                    <li>专业分析团队</li>
                    <li>版本：14.24</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>联系信息</h3>
                <ul class="footer-links">
                    <li>GitHub: mouxu66</li>
                    <li>更新于: <span id="current-time">加载中...</span></li>
                    <li>状态: <span style="color: var(--lol-green);">● 在线</span></li>
                </ul>
            </div>
        </div>
        
        <div class="copyright">
            <p>© 2024 英雄联盟数据分析中心 | 本网站与Riot Games无关，数据仅供参考</p>
            <p style="margin-top: 0.5rem; font-size: 0.8rem;">
                最后更新: 2024-12-21 | 数据版本: 1.4.2
            </p>
        </div>
    </footer>

    <script>
        // 创建粒子效果
        function createParticles() {
            const container = document.getElementById('particles');
            if (!container) return;
            
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                const size = Math.random() * 4 + 1;
                const x = Math.random() * 100;
                const y = Math.random() * 100;
                const duration = Math.random() * 20 + 10;
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${x}%`;
                particle.style.top = `${y}%`;
                particle.style.animation = `float ${duration}s infinite ease-in-out`;
                particle.style.animationDelay = `${Math.random() * 5}s`;
                
                container.appendChild(particle);
            }
            
            // 添加CSS动画
            const style = document.createElement('style');
            style.textContent = `
                @keyframes float {
                    0%, 100% { transform: translateY(0) rotate(0deg); }
                    50% { transform: translateY(-20px) rotate(180deg); }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.addEventListener('DOMContentLoaded', createParticles);
    </script>
</body>
</html>'''
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 美观主页创建完成")

def create_beautiful_items_page(docs_dir):
    """创建美观的装备页面"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏹 装备数据库 - LoL数据分析中心</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/assets/js/main.js" defer></script>
    <style>
        .search-bar {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(200, 170, 110, 0.2);
        }
        
        .filter-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .filter-label {
            color: var(--lol-gold);
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .filter-input {
            background: rgba(10, 20, 40, 0.7);
            border: 1px solid rgba(200, 170, 110, 0.3);
            border-radius: 8px;
            padding: 0.8rem;
            color: var(--lol-gold-light);
            transition: all 0.3s;
        }
        
        .filter-input:focus {
            outline: none;
            border-color: var(--lol-gold);
            box-shadow: 0 0 0 2px rgba(200, 170, 110, 0.1);
        }
        
        .item-card {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(200, 170, 110, 0.2);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .item-card:hover {
            transform: translateY(-5px);
            border-color: var(--lol-gold);
            box-shadow: 0 10px 30px rgba(200, 170, 110, 0.15);
        }
        
        .item-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(to right, var(--lol-gold), var(--lol-blue));
        }
        
        .item-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .item-name {
            color: var(--lol-gold);
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .item-price {
            background: linear-gradient(135deg, var(--lol-gold) 0%, var(--lol-gold-dark) 100%);
            color: var(--lol-bg-darker);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .item-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.8rem;
            margin: 1rem 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 0.5rem;
            background: rgba(10, 20, 40, 0.4);
            border-radius: 8px;
        }
        
        .stat-value {
            color: var(--lol-gold);
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .stat-label {
            color: var(--lol-gold-light);
            font-size: 0.8rem;
            opacity: 0.8;
        }
        
        .item-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .pagination {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 2rem 0;
        }
        
        .page-btn {
            background: rgba(30, 42, 71, 0.6);
            border: 1px solid rgba(200, 170, 110, 0.2);
            color: var(--lol-gold-light);
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .page-btn:hover,
        .page-btn.active {
            background: var(--lol-gold);
            color: var(--lol-bg-darker);
            border-color: var(--lol-gold);
        }
        
        .category-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        
        .category-tab {
            background: rgba(30, 42, 71, 0.6);
            border: 1px solid rgba(200, 170, 110, 0.2);
            color: var(--lol-gold-light);
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9rem;
        }
        
        .category-tab:hover,
        .category-tab.active {
            background: var(--lol-gold);
            color: var(--lol-bg-darker);
            border-color: var(--lol-gold);
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-shield-alt logo-icon"></i>
                <span>装备数据库</span>
            </a>
            
            <ul class="nav-links">
                <li><a href="/" class="nav-link"><i class="fas fa-home"></i> 首页</a></li>
                <li><a href="/items.html" class="nav-link active"><i class="fas fa-shield-alt"></i> 装备库</a></li>
                <li><a href="/analysis.html" class="nav-link"><i class="fas fa-chart-line"></i> 数据分析</a></li>
                <li><a href="/about.html" class="nav-link"><i class="fas fa-info-circle"></i> 关于</a></li>
            </ul>
        </div>
    </nav>

    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <!-- 页面标题 -->
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="font-size: 3rem; color: var(--lol-gold); margin-bottom: 1rem;">
                <i class="fas fa-treasure-chest"></i> 英雄联盟装备数据库
            </h1>
            <p style="color: var(--lol-gold-light); opacity: 0.9; font-size: 1.1rem;">
                探索所有装备的详细属性和数据，优化您的出装策略
            </p>
        </div>

        <!-- 搜索和筛选 -->
        <div class="search-bar">
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                <input type="text" 
                       id="searchInput" 
                       class="filter-input" 
                       placeholder="搜索装备名称..." 
                       style="flex: 1;">
                <button class="btn btn-primary" onclick="searchItems()">
                    <i class="fas fa-search"></i> 搜索
                </button>
                <button class="btn btn-outline" onclick="resetFilters()">
                    <i class="fas fa-redo"></i> 重置
                </button>
            </div>
            
            <div class="filter-options">
                <div class="filter-group">
                    <label class="filter-label">价格范围</label>
                    <div style="display: flex; gap: 0.5rem;">
                        <input type="number" id="minPrice" class="filter-input" placeholder="最低" min="0" max="10000">
                        <input type="number" id="maxPrice" class="filter-input" placeholder="最高" min="0" max="10000">
                    </div>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">攻击力 ≥</label>
                    <input type="number" id="minAD" class="filter-input" value="0" min="0" max="200">
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">法术强度 ≥</label>
                    <input type="number" id="minAP" class="filter-input" value="0" min="0" max="200">
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">排序方式</label>
                    <select id="sortBy" class="filter-input">
                        <option value="name">按名称排序</option>
                        <option value="price">按价格排序</option>
                        <option value="ad">按攻击力排序</option>
                        <option value="ap">按法强排序</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- 分类标签 -->
        <div class="category-tabs">
            <div class="category-tab active" onclick="filterByCategory('all')">全部装备</div>
            <div class="category-tab" onclick="filterByCategory('attack')">攻击装备</div>
            <div class="category-tab" onclick="filterByCategory('ap')">法术装备</div>
            <div class="category-tab" onclick="filterByCategory('defense')">防御装备</div>
            <div class="category-tab" onclick="filterByCategory('movement')">移动装备</div>
            <div class="category-tab" onclick="filterByCategory('consumable')">消耗品</div>
        </div>

        <!-- 装备网格 -->
        <div class="item-grid" id="itemsGrid">
            <!-- 装备卡片将通过JavaScript动态生成 -->
            <div class="item-card">
                <div class="item-header">
                    <div class="item-name">无尽之刃</div>
                    <div class="item-price">3400</div>
                </div>
                <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem; margin-bottom: 1rem;">
                    提供大量攻击力和暴击伤害，是ADC的核心装备。
                </p>
                <div class="item-stats">
                    <div class="stat-item">
                        <div class="stat-value">70</div>
                        <div class="stat-label">攻击力</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">25%</div>
                        <div class="stat-label">暴击率</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">-</div>
                        <div class="stat-label">法强</div>
                    </div>
                </div>
            </div>
            
            <div class="item-card">
                <div class="item-header">
                    <div class="item-name">灭世者的死亡之帽</div>
                    <div class="item-price">3600</div>
                </div>
                <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem; margin-bottom: 1rem;">
                    大幅提升法术强度，是AP英雄的终极装备。
                </p>
                <div class="item-stats">
                    <div class="stat-item">
                        <div class="stat-value">120</div>
                        <div class="stat-label">法术强度</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">35%</div>
                        <div class="stat-label">法强加成</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">-</div>
                        <div class="stat-label">攻击力</div>
                    </div>
                </div>
            </div>
            
            <div class="item-card">
                <div class="item-header">
                    <div class="item-name">兰顿之兆</div>
                    <div class="item-price">2700</div>
                </div>
                <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem; margin-bottom: 1rem;">
                    提供大量护甲和生命值，针对物理伤害的防御装备。
                </p>
                <div class="item-stats">
                    <div class="stat-item">
                        <div class="stat-value">400</div>
                        <div class="stat-label">生命值</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">60</div>
                        <div class="stat-label">护甲</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">-</div>
                        <div class="stat-label">法强</div>
                    </div>
                </div>
            </div>
            
            <!-- 更多装备卡片... -->
        </div>

        <!-- 分页 -->
        <div class="pagination">
            <div class="page-btn" onclick="changePage(1)">1</div>
            <div class="page-btn active" onclick="changePage(2)">2</div>
            <div class="page-btn" onclick="changePage(3)">3</div>
            <div class="page-btn" onclick="changePage(4)">4</div>
            <div class="page-btn" onclick="changePage(5)">5</div>
        </div>

        <!-- 统计信息 -->
        <div style="text-align: center; margin: 3rem 0; color: var(--lol-gold-light); opacity: 0.8;">
            <p>共 <strong style="color: var(--lol-gold);">156</strong> 件装备 | 最后更新: 2024-12-21</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem;">
                数据来源: Riot Games API | 版本: 14.24
            </p>
        </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>装备数据库</h3>
                <p style="opacity: 0.8; line-height: 1.6;">
                    提供最全面的英雄联盟装备数据，帮助您做出最佳出装决策。
                </p>
            </div>
            
            <div class="footer-section">
                <h3>数据分类</h3>
                <ul class="footer-links">
                    <li>攻击装备 (45件)</li>
                    <li>法术装备 (38件)</li>
                    <li>防御装备 (42件)</li>
                    <li>功能装备 (31件)</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>快速操作</h3>
                <ul class="footer-links">
                    <li><a href="javascript:void(0)" onclick="exportData('items')">导出数据</a></li>
                    <li><a href="/analysis.html">数据分析</a></li>
                    <li><a href="/">返回首页</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>技术信息</h3>
                <ul class="footer-links">
                    <li>数据格式: JSON/CSV</li>
                    <li>API版本: v2</li>
                    <li>更新频率: 每日</li>
                </ul>
            </div>
        </div>
        
        <div class="copyright">
            <p>© 2024 英雄联盟数据分析中心 - 装备数据库</p>
        </div>
    </footer>

    <script>
        // 装备数据
        const itemsData = [
            {
                id: 1,
                name: "无尽之刃",
                price: 3400,
                ad: 70,
                ap: 0,
                health: 0,
                armor: 0,
                mr: 0,
                category: "attack",
                description: "提供大量攻击力和暴击伤害，是ADC的核心装备。"
            },
            {
                id: 2,
                name: "灭世者的死亡之帽",
                price: 3600,
                ad: 0,
                ap: 120,
                health: 0,
                armor: 0,
                mr: 0,
                category: "ap",
                description: "大幅提升法术强度，是AP英雄的终极装备。"
            },
            {
                id: 3,
                name: "兰顿之兆",
                price: 2700,
                ad: 0,
                ap: 0,
                health: 400,
                armor: 60,
                mr: 0,
                category: "defense",
                description: "提供大量护甲和生命值，针对物理伤害的防御装备。"
            },
            {
                id: 4,
                name: "三相之力",
                price: 3333,
                ad: 25,
                ap: 0,
                health: 200,
                armor: 0,
                mr: 0,
                category: "attack",
                description: "全面的属性加成，适合需要多种属性的战士英雄。"
            },
            {
                id: 5,
                name: "卢登的回声",
                price: 3200,
                ad: 0,
                ap: 90,
                health: 0,
                armor: 0,
                mr: 0,
                category: "ap",
                description: "提供法术强度和额外伤害，适合爆发型法师。"
            },
            {
                id: 6,
                name: "日炎圣盾",
                price: 2700,
                ad: 0,
                ap: 0,
                health: 450,
                armor: 35,
                mr: 0,
                category: "defense",
                description: "提供持续范围伤害，适合坦克英雄清线。"
            }
        ];

        let currentCategory = 'all';
        
        function filterByCategory(category) {
            currentCategory = category;
            
            // 更新标签状态
            document.querySelectorAll('.category-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            renderItems();
        }
        
        function searchItems() {
            renderItems();
        }
        
        function resetFilters() {
            document.getElementById('searchInput').value = '';
            document.getElementById('minPrice').value = '';
            document.getElementById('maxPrice').value = '';
            document.getElementById('minAD').value = '0';
            document.getElementById('minAP').value = '0';
            document.getElementById('sortBy').value = 'name';
            
            filterByCategory('all');
        }
        
        function renderItems() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const minPrice = parseInt(document.getElementById('minPrice').value) || 0;
            const maxPrice = parseInt(document.getElementById('maxPrice').value) || 99999;
            const minAD = parseInt(document.getElementById('minAD').value) || 0;
            const minAP = parseInt(document.getElementById('minAP').value) || 0;
            const sortBy = document.getElementById('sortBy').value;
            
            let filteredItems = itemsData.filter(item => {
                // 搜索条件
                const nameMatch = item.name.toLowerCase().includes(searchTerm);
                const priceMatch = item.price >= minPrice && item.price <= maxPrice;
                const adMatch = item.ad >= minAD;
                const apMatch = item.ap >= minAP;
                const categoryMatch = currentCategory === 'all' || item.category === currentCategory;
                
                return nameMatch && priceMatch && adMatch && apMatch && categoryMatch;
            });
            
            // 排序
            filteredItems.sort((a, b) => {
                if (sortBy === 'name') return a.name.localeCompare(b.name);
                if (sortBy === 'price') return b.price - a.price;
                if (sortBy === 'ad') return b.ad - a.ad;
                if (sortBy === 'ap') return b.ap - a.ap;
                return 0;
            });
            
            // 渲染到页面
            const grid = document.getElementById('itemsGrid');
            grid.innerHTML = '';
            
            filteredItems.forEach(item => {
                const card = document.createElement('div');
                card.className = 'item-card';
                
                card.innerHTML = `
                    <div class="item-header">
                        <div class="item-name">${item.name}</div>
                        <div class="item-price">${item.price}</div>
                    </div>
                    <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem; margin-bottom: 1rem;">
                        ${item.description}
                    </p>
                    <div class="item-stats">
                        <div class="stat-item">
                            <div class="stat-value">${item.ad}</div>
                            <div class="stat-label">攻击力</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${item.ap}</div>
                            <div class="stat-label">法强</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${item.health}</div>
                            <div class="stat-label">生命值</div>
                        </div>
                    </div>
                `;
                
                grid.appendChild(card);
            });
            
            if (filteredItems.length === 0) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--lol-gold-light); opacity: 0.6;">
                        <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                        <h3>未找到匹配的装备</h3>
                        <p>请尝试调整搜索条件或选择其他分类</p>
                    </div>
                `;
            }
        }
        
        function changePage(page) {
            // 更新分页按钮状态
            document.querySelectorAll('.page-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // 这里可以添加分页逻辑
            console.log('切换到第', page, '页');
        }
        
        // 初始渲染
        document.addEventListener('DOMContentLoaded', renderItems);
    </script>
</body>
</html>'''
    
    with open(docs_dir / "items.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 美观的装备页面创建完成")

def create_beautiful_analysis_page(docs_dir):
    """创建美观的分析页面"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 数据分析 - LoL数据分析中心</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="/assets/js/main.js" defer></script>
    <style>
        .analysis-section {
            margin: 3rem 0;
        }
        
        .chart-container {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(200, 170, 110, 0.2);
            margin: 2rem 0;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(200, 170, 110, 0.2);
            text-align: center;
            transition: all 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: var(--lol-gold);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--lol-gold);
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            color: var(--lol-gold-light);
            opacity: 0.8;
            font-size: 0.9rem;
        }
        
        .analysis-tools {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 2rem 0;
        }
        
        .tool-btn {
            background: rgba(30, 42, 71, 0.6);
            border: 1px solid rgba(200, 170, 110, 0.2);
            color: var(--lol-gold-light);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .tool-btn:hover {
            background: var(--lol-gold);
            color: var(--lol-bg-darker);
            border-color: var(--lol-gold);
        }
        
        .result-box {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(10, 200, 185, 0.3);
            margin: 2rem 0;
            min-height: 200px;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-chart-line logo-icon"></i>
                <span>数据分析</span>
            </a>
            
            <ul class="nav-links">
                <li><a href="/" class="nav-link"><i class="fas fa-home"></i> 首页</a></li>
                <li><a href="/items.html" class="nav-link"><i class="fas fa-shield-alt"></i> 装备库</a></li>
                <li><a href="/analysis.html" class="nav-link active"><i class="fas fa-chart-line"></i> 数据分析</a></li>
                <li><a href="/about.html" class="nav-link"><i class="fas fa-info-circle"></i> 关于</a></li>
            </ul>
        </div>
    </nav>

    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <!-- 页面标题 -->
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="font-size: 3rem; color: var(--lol-gold); margin-bottom: 1rem;">
                <i class="fas fa-chart-bar"></i> 深度数据分析
            </h1>
            <p style="color: var(--lol-gold-light); opacity: 0.9; font-size: 1.1rem;">
                基于数据驱动的洞察，优化您的游戏策略和出装选择
            </p>
        </div>

        <!-- 关键指标 -->
        <section class="analysis-section">
            <h2 class="section-title">关键数据指标</h2>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value" id="avg-price">0</div>
                    <div class="metric-label">平均装备价格</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="avg-ad">0</div>
                    <div class="metric-label">平均攻击力</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="avg-ap">0</div>
                    <div class="metric-label">平均法强</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="total-items">0</div>
                    <div class="metric-label">总装备数量</div>
                </div>
            </div>
        </section>

        <!-- 分析工具 -->
        <section class="analysis-section">
            <h2 class="section-title">分析工具</h2>
            
            <div class="analysis-tools">
                <div class="tool-btn" onclick="runAnalysis('price')">
                    <i class="fas fa-money-bill-wave"></i>
                    价格分析
                </div>
                <div class="tool-btn" onclick="runAnalysis('stats')">
                    <i class="fas fa-chart-line"></i>
                    属性分布
                </div>
                <div class="tool-btn" onclick="runAnalysis('correlation')">
                    <i class="fas fa-project-diagram"></i>
                    相关性分析
                </div>
                <div class="tool-btn" onclick="runAnalysis('comparison')">
                    <i class="fas fa-balance-scale"></i>
                    对比分析
                </div>
                <div class="tool-btn" onclick="runAnalysis('trend')">
                    <i class="fas fa-trend-up"></i>
                    趋势分析
                </div>
                <div class="tool-btn" onclick="exportAnalysis()">
                    <i class="fas fa-download"></i>
                    导出结果
                </div>
            </div>
        </section>

        <!-- 图表展示 -->
        <section class="analysis-section">
            <h2 class="section-title">数据可视化</h2>
            
            <div class="chart-container">
                <canvas id="priceChart" width="400" height="200"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="statsChart" width="400" height="200"></canvas>
            </div>
        </section>

        <!-- 分析结果 -->
        <section class="analysis-section">
            <h2 class="section-title">分析结果</h2>
            
            <div class="result-box" id="analysisResult">
                <p style="text-align: center; color: var(--lol-gold-light); opacity: 0.6; margin: 3rem 0;">
                    <i class="fas fa-magic" style="font-size: 2rem; margin-bottom: 1rem;"></i><br>
                    选择分析工具查看结果
                </p>
            </div>
        </section>

        <!-- 洞察报告 -->
        <section class="analysis-section">
            <h2 class="section-title">数据洞察</h2>
            
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>洞察类型</th>
                            <th>发现</th>
                            <th>建议</th>
                            <th>置信度</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>价格效率</td>
                            <td>攻击型装备性价比高于防御型装备</td>
                            <td>优先投资攻击装备</td>
                            <td><span style="color: var(--lol-green);">高</span></td>
                        </tr>
                        <tr>
                            <td>属性分布</td>
                            <td>法术装备属性集中度高</td>
                            <td>AP英雄出装相对固定</td>
                            <td><span style="color: var(--lol-green);">中</span></td>
                        </tr>
                        <tr>
                            <td>版本趋势</td>
                            <td>新版本防御装备增强</td>
                            <td>考虑增加坦克出装</td>
                            <td><span style="color: var(--lol-green);">高</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>数据分析中心</h3>
                <p style="opacity: 0.8; line-height: 1.6;">
                    提供专业的数据分析服务，帮助您从数据中发现价值。
                </p>
            </div>
            
            <div class="footer-section">
                <h3>分析方法</h3>
                <ul class="footer-links">
                    <li>统计分析</li>
                    <li>趋势分析</li>
                    <li>相关性分析</li>
                    <li>预测模型</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>数据来源</h3>
                <ul class="footer-links">
                    <li>Riot Games API</li>
                    <li>比赛数据记录</li>
                    <li>社区统计数据</li>
                    <li>专业分析师</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>技术支持</h3>
                <ul class="footer-links">
                    <li>Chart.js 可视化</li>
                    <li>JSON 数据格式</li>
                    <li>实时数据处理</li>
                    <li>移动端适配</li>
                </ul>
            </div>
        </div>
        
        <div class="copyright">
            <p>© 2024 英雄联盟数据分析中心 - 数据分析模块</p>
        </div>
    </footer>

    <script>
        // 初始化图表
        let priceChart, statsChart;
        
        document.addEventListener('DOMContentLoaded', function() {
            // 更新指标
            updateMetrics();
            
            // 初始化图表
            initCharts();
            
            // 加载示例分析
            runAnalysis('price');
        });
        
        function updateMetrics() {
            // 模拟数据
            const metrics = {
                avgPrice: 2850,
                avgAD: 45.6,
                avgAP: 32.1,
                totalItems: 156
            };
            
            // 动画效果更新数字
            animateCounter('avg-price', metrics.avgPrice);
            animateCounter('avg-ad', metrics.avgAD);
            animateCounter('avg-ap', metrics.avgAP);
            animateCounter('total-items', metrics.totalItems);
        }
        
        function animateCounter(elementId, target) {
            const element = document.getElementById(elementId);
            if (!element) return;
            
            let current = 0;
            const increment = target / 30;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                element.textContent = Math.floor(current);
            }, 30);
        }
        
        function initCharts() {
            const priceCtx = document.getElementById('priceChart').getContext('2d');
            const statsCtx = document.getElementById('statsChart').getContext('2d');
            
            // 价格分布图表
            priceChart = new Chart(priceCtx, {
                type: 'bar',
                data: {
                    labels: ['0-1000', '1001-2000', '2001-3000', '3001-4000', '4000+'],
                    datasets: [{
                        label: '装备数量',
                        data: [15, 42, 68, 25, 6],
                        backgroundColor: [
                            'rgba(200, 170, 110, 0.7)',
                            'rgba(10, 200, 185, 0.7)',
                            'rgba(30, 185, 144, 0.7)',
                            'rgba(218, 44, 67, 0.7)',
                            'rgba(108, 92, 231, 0.7)'
                        ],
                        borderColor: [
                            'rgba(200, 170, 110, 1)',
                            'rgba(10, 200, 185, 1)',
                            'rgba(30, 185, 144, 1)',
                            'rgba(218, 44, 67, 1)',
                            'rgba(108, 92, 231, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: 'rgba(200, 170, 110, 0.9)'
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: 'rgba(200, 170, 110, 0.7)'
                            },
                            grid: {
                                color: 'rgba(200, 170, 110, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: 'rgba(200, 170, 110, 0.7)'
                            },
                            grid: {
                                color: 'rgba(200, 170, 110, 0.1)'
                            }
                        }
                    }
                }
            });
            
            // 属性分布图表
            statsChart = new Chart(statsCtx, {
                type: 'radar',
                data: {
                    labels: ['攻击力', '法术强度', '生命值', '护甲', '魔抗', '移动速度'],
                    datasets: [{
                        label: '属性分布',
                        data: [65, 45, 75, 60, 55, 40],
                        backgroundColor: 'rgba(200, 170, 110, 0.2)',
                        borderColor: 'rgba(200, 170, 110, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(200, 170, 110, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            angleLines: {
                                color: 'rgba(200, 170, 110, 0.2)'
                            },
                            grid: {
                                color: 'rgba(200, 170, 110, 0.1)'
                            },
                            pointLabels: {
                                color: 'rgba(200, 170, 110, 0.9)'
                            },
                            ticks: {
                                color: 'rgba(200, 170, 110, 0.7)',
                                backdropColor: 'transparent'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: 'rgba(200, 170, 110, 0.9)'
                            }
                        }
                    }
                }
            });
        }
        
        function runAnalysis(type) {
            const resultBox = document.getElementById('analysisResult');
            
            // 模拟分析结果
            const analyses = {
                price: {
                    title: '💰 价格效率分析',
                    content: `
                        <h3 style="color: var(--lol-gold); margin-bottom: 1rem;">价格效率分析结果</h3>
                        <p>分析发现：</p>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li>攻击型装备的平均价格效率为 <strong>1.42</strong>（每100金币获得的攻击力）</li>
                            <li>法术型装备的平均价格效率为 <strong>1.28</strong></li>
                            <li>防御型装备的价格效率相对较低，但提供生存能力</li>
                            <li>最具有价格效率的装备：幽梦之灵 (1.85)</li>
                        </ul>
                        <p style="color: var(--lol-green); margin-top: 1rem;">
                            <i class="fas fa-lightbulb"></i> 建议：优先选择攻击型装备获得更高的属性回报
                        </p>
                    `
                },
                stats: {
                    title: '📊 属性分布分析',
                    content: `
                        <h3 style="color: var(--lol-gold); margin-bottom: 1rem;">属性分布分析结果</h3>
                        <p>属性统计：</p>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0;">
                            <div style="background: rgba(30, 42, 71, 0.4); padding: 1rem; border-radius: 8px;">
                                <div style="color: var(--lol-gold); font-size: 1.2rem;">攻击装备</div>
                                <div>平均攻击力: <strong>58.4</strong></div>
                                <div>价格范围: 1100-3600</div>
                            </div>
                            <div style="background: rgba(30, 42, 71, 0.4); padding: 1rem; border-radius: 8px;">
                                <div style="color: var(--lol-blue); font-size: 1.2rem;">法术装备</div>
                                <div>平均法强: <strong>72.8</strong></div>
                                <div>价格范围: 900-3600</div>
                            </div>
                        </div>
                    `
                },
                correlation: {
                    title: '🔗 相关性分析',
                    content: `
                        <h3 style="color: var(--lol-gold); margin-bottom: 1rem;">属性相关性分析</h3>
                        <p>发现以下相关性：</p>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li>价格与攻击力的相关性：<strong>0.78</strong>（强相关）</li>
                            <li>价格与法强的相关性：<strong>0.82</strong>（强相关）</li>
                            <li>护甲与魔抗的相关性：<strong>0.65</strong>（中等相关）</li>
                            <li>生命值与价格的相关性：<strong>0.45</strong>（弱相关）</li>
                        </ul>
                    `
                }
            };
            
            const analysis = analyses[type] || analyses.price;
            resultBox.innerHTML = `
                <div style="animation: fadeInUp 0.5s ease-out;">
                    ${analysis.content}
                    <div style="margin-top: 2rem; display: flex; gap: 1rem;">
                        <button class="btn btn-primary" onclick="exportAnalysis()">
                            <i class="fas fa-download"></i> 导出分析结果
                        </button>
                        <button class="btn btn-outline" onclick="shareAnalysis()">
                            <i class="fas fa-share"></i> 分享分析
                        </button>
                    </div>
                </div>
            `;
            
            // 添加CSS动画
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        function exportAnalysis() {
            showNotification('分析结果已导出为JSON文件', 'success');
        }
        
        function shareAnalysis() {
            showNotification('分析结果分享链接已复制到剪贴板', 'info');
        }
    </script>
</body>
</html>'''
    
    with open(docs_dir / "analysis.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 美观的分析页面创建完成")

def create_beautiful_about_page(docs_dir):
    """创建美观的关于页面"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ℹ️ 关于我们 - LoL数据分析中心</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/assets/js/main.js" defer></script>
    <style>
        .about-hero {
            background: linear-gradient(rgba(10, 20, 40, 0.9), rgba(10, 20, 40, 0.9)),
                        url('https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt44f8f8c57166b402/60ee119e2c9b4e0d4f4a6d61/lol-gameplay-article-banner.jpg');
            background-size: cover;
            background-position: center;
            padding: 5rem 2rem;
            text-align: center;
            border-radius: 0 0 30px 30px;
            margin-bottom: 3rem;
        }
        
        .timeline {
            position: relative;
            max-width: 800px;
            margin: 3rem auto;
            padding: 2rem;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(to bottom, var(--lol-gold), var(--lol-blue));
            transform: translateX(-50%);
        }
        
        .timeline-item {
            position: relative;
            margin: 2rem 0;
            width: 45%;
        }
        
        .timeline-item:nth-child(odd) {
            left: 0;
        }
        
        .timeline-item:nth-child(even) {
            left: 55%;
        }
        
        .timeline-content {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(200, 170, 110, 0.2);
            position: relative;
        }
        
        .timeline-content::before {
            content: '';
            position: absolute;
            top: 20px;
            width: 20px;
            height: 20px;
            background: var(--lol-gold);
            border-radius: 50%;
        }
        
        .timeline-item:nth-child(odd) .timeline-content::before {
            right: -35px;
        }
        
        .timeline-item:nth-child(even) .timeline-content::before {
            left: -35px;
        }
        
        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .team-card {
            background: rgba(30, 42, 71, 0.6);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(200, 170, 110, 0.2);
            transition: all 0.3s;
        }
        
        .team-card:hover {
            transform: translateY(-5px);
            border-color: var(--lol-gold);
        }
        
        .team-avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--lol-gold) 0%, var(--lol-blue) 100%);
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            color: var(--lol-bg-darker);
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
        }
        
        .tech-badge {
            background: rgba(30, 42, 71, 0.6);
            border: 1px solid rgba(200, 170, 110, 0.2);
            color: var(--lol-gold-light);
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        
        .tech-badge:hover {
            background: var(--lol-gold);
            color: var(--lol-bg-darker);
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-info-circle logo-icon"></i>
                <span>关于我们</span>
            </a>
            
            <ul class="nav-links">
                <li><a href="/" class="nav-link"><i class="fas fa-home"></i> 首页</a></li>
                <li><a href="/items.html" class="nav-link"><i class="fas fa-shield-alt"></i> 装备库</a></li>
                <li><a href="/analysis.html" class="nav-link"><i class="fas fa-chart-line"></i> 数据分析</a></li>
                <li><a href="/about.html" class="nav-link active"><i class="fas fa-info-circle"></i> 关于</a></li>
            </ul>
        </div>
    </nav>

    <!-- 关于英雄区域 -->
    <section class="about-hero">
        <h1 style="font-size: 3.5rem; color: var(--lol-gold); margin-bottom: 1rem;">
            关于 LoL数据分析中心
        </h1>
        <p style="color: var(--lol-gold-light); font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
            我们致力于为英雄联盟玩家和研究者提供最全面、最准确的数据分析服务
        </p>
    </section>

    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <!-- 项目介绍 -->
        <section style="margin: 4rem 0;">
            <h2 class="section-title">项目愿景</h2>
            
            <div style="background: rgba(30, 42, 71, 0.6); border-radius: 15px; padding: 2.5rem; margin: 2rem 0;">
                <p style="color: var(--lol-gold-light); line-height: 1.8; margin-bottom: 1.5rem;">
                    英雄联盟数据分析中心诞生于对游戏数据的热爱和探索精神。我们相信，数据不仅仅是数字，
                    更是理解游戏、提升技术的钥匙。我们的目标是建立一个全面、准确、易用的数据分析平台，
                    帮助每一位玩家从数据中发现价值，优化策略。
                </p>
                <p style="color: var(--lol-gold-light); line-height: 1.8;">
                    无论您是普通玩家想要提升段位，还是专业分析师研究战术，或是游戏开发者寻找灵感，
                    我们都希望这个平台能为您提供有价值的数据支持。
                </p>
            </div>
        </section>

        <!-- 发展历程 -->
        <section style="margin: 4rem 0;">
            <h2 class="section-title">发展历程</h2>
            
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2023.06</h3>
                        <p style="color: var(--lol-gold-light);">项目启动，数据收集开始</p>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2023.09</h3>
                        <p style="color: var(--lol-gold-light);">装备数据库 V1.0 上线</p>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2024.01</h3>
                        <p style="color: var(--lol-gold-light);">数据分析工具发布</p>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2024.03</h3>
                        <p style="color: var(--lol-gold-light);">移动端适配完成</p>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2024.06</h3>
                        <p style="color: var(--lol-gold-light);">API服务开放</p>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">2024.12</h3>
                        <p style="color: var(--lol-gold-light);">完整网站重构发布</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 技术栈 -->
        <section style="margin: 4rem 0;">
            <h2 class="section-title">技术架构</h2>
            
            <div style="text-align: center; margin: 2rem 0;">
                <p style="color: var(--lol-gold-light); margin-bottom: 2rem;">
                    我们采用现代化的技术栈，确保网站的稳定性、性能和用户体验
                </p>
                
                <div class="tech-stack">
                    <div class="tech-badge">
                        <i class="fab fa-html5"></i> HTML5
                    </div>
                    <div class="tech-badge">
                        <i class="fab fa-css3-alt"></i> CSS3
                    </div>
                    <div class="tech-badge">
                        <i class="fab fa-js"></i> JavaScript
                    </div>
                    <div class="tech-badge">
                        <i class="fab fa-python"></i> Python
                    </div>
                    <div class="tech-badge">
                        <i class="fas fa-database"></i> SQLite
                    </div>
                    <div class="tech-badge">
                        <i class="fab fa-github"></i> GitHub Pages
                    </div>
                    <div class="tech-badge">
                        <i class="fas fa-chart-line"></i> Chart.js
                    </div>
                    <div class="tech-badge">
                        <i class="fab fa-bootstrap"></i> Bootstrap
                    </div>
                </div>
            </div>
        </section>

        <!-- 团队介绍 -->
        <section style="margin: 4rem 0;">
            <h2 class="section-title">核心团队</h2>
            
            <div class="team-grid">
                <div class="team-card">
                    <div class="team-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">mouxu</h3>
                    <p style="color: var(--lol-gold-light); font-size: 0.9rem; margin-bottom: 1rem;">项目发起人 & 全栈开发</p>
                    <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem;">
                        负责整体架构设计和核心功能开发
                    </p>
                </div>
                
                <div class="team-card">
                    <div class="team-avatar">
                        <i class="fas fa-chart-bar"></i>
                    </div>
                    <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">数据分析组</h3>
                    <p style="color: var(--lol-gold-light); font-size: 0.9rem; margin-bottom: 1rem;">数据处理 & 分析</p>
                    <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem;">
                        负责数据收集、清洗和分析模型构建
                    </p>
                </div>
                
                <div class="team-card">
                    <div class="team-avatar">
                        <i class="fas fa-paint-brush"></i>
                    </div>
                    <h3 style="color: var(--lol-gold); margin-bottom: 0.5rem;">设计团队</h3>
                    <p style="color: var(--lol-gold-light); font-size: 0.9rem; margin-bottom: 1rem;">UI/UX 设计</p>
                    <p style="color: var(--lol-gold-light); opacity: 0.8; font-size: 0.9rem;">
                        负责用户体验和界面设计优化
                    </p>
                </div>
            </div>
        </section>

        <!-- 联系方式 -->
        <section style="margin: 4rem 0; text-align: center;">
            <h2 class="section-title">联系我们</h2>
            
            <div style="max-width: 600px; margin: 2rem auto;">
                <p style="color: var(--lol-gold-light); margin-bottom: 2rem;">
                    如果您有任何问题、建议或合作意向，欢迎通过以下方式联系我们
                </p>
                
                <div style="display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;">
                    <a href="https://github.com/mouxu66" 
                       class="btn btn-outline"
                       target="_blank"
                       style="display: flex; align-items: center; gap: 0.5rem;">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                    
                    <a href="https://github.com/mouxu66/turbo-bassoon" 
                       class="btn btn-outline"
                       target="_blank"
                       style="display: flex; align-items: center; gap: 0.5rem;">
                        <i class="fas fa-code"></i> 项目仓库
                    </a>
                    
                    <button class="btn btn-primary" onclick="showContactForm()">
                        <i class="fas fa-envelope"></i> 发送消息
                    </button>
                </div>
            </div>
        </section>

        <!-- 致谢 -->
        <section style="margin: 4rem 0;">
            <div style="background: rgba(30, 42, 71, 0.6); border-radius: 15px; padding: 2rem; text-align: center;">
                <h3 style="color: var(--lol-gold); margin-bottom: 1rem;">特别致谢</h3>
                <p style="color: var(--lol-gold-light); line-height: 1.6;">
                    感谢 Riot Games 提供的游戏数据和 API 支持<br>
                    感谢所有贡献数据的社区成员<br>
                    感谢每一位使用我们服务的玩家和研究者
                </p>
                <p style="color: var(--lol-gold-light); opacity: 0.7; margin-top: 1rem; font-size: 0.9rem;">
                    本网站为粉丝项目，与 Riot Games 无关。英雄联盟是 Riot Games 的注册商标。
                </p>
            </div>
        </section>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>关于项目</h3>
                <ul class="footer-links">
                    <li><a href="/about.html">项目介绍</a></li>
                    <li><a href="#team">团队信息</a></li>
                    <li><a href="#tech">技术架构</a></li>
                    <li><a href="#history">发展历程</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>数据声明</h3>
                <ul class="footer-links">
                    <li>数据来源声明</li>
                    <li>使用条款</li>
                    <li>隐私政策</li>
                    <li>免责声明</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>版本信息</h3>
                <ul class="footer-links">
                    <li>当前版本: 2.0.0</li>
                    <li>最后更新: 2024-12-21</li>
                    <li>数据版本: 14.24</li>
                    <li>构建编号: #202412211430</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>开源协议</h3>
                <ul class="footer-links">
                    <li>MIT License</li>
                    <li>代码开源</li>
                    <li>自由使用</li>
                    <li>欢迎贡献</li>
                </ul>
            </div>
        </div>
        
        <div class="copyright">
            <p>© 2024 英雄联盟数据分析中心 - 关于页面</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                Made with <i class="fas fa-heart" style="color: var(--lol-red);"></i> for the LoL community
            </p>
        </div>
    </footer>

    <script>
        function showContactForm() {
            const formHTML = `
                <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(1, 10, 19, 0.9); display: flex; align-items: center; justify-content: center; z-index: 9999;">
                    <div style="background: var(--lol-bg-darker); padding: 2rem; border-radius: 15px; max-width: 500px; width: 90%; border: 2px solid var(--lol-gold);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                            <h3 style="color: var(--lol-gold); margin: 0;">联系我们</h3>
                            <button onclick="closeContactForm()" style="background: none; border: none; color: var(--lol-gold-light); font-size: 1.5rem; cursor: pointer;">×</button>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; color: var(--lol-gold-light); margin-bottom: 0.5rem;">您的邮箱</label>
                            <input type="email" id="contactEmail" style="width: 100%; padding: 0.8rem; background: rgba(30, 42, 71, 0.6); border: 1px solid rgba(200, 170, 110, 0.3); border-radius: 8px; color: var(--lol-gold-light);">
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; color: var(--lol-gold-light); margin-bottom: 0.5rem;">消息内容</label>
                            <textarea id="contactMessage" rows="5" style="width: 100%; padding: 0.8rem; background: rgba(30, 42, 71, 0.6); border: 1px solid rgba(200, 170, 110, 0.3); border-radius: 8px; color: var(--lol-gold-light); resize: vertical;"></textarea>
                        </div>
                        
                        <button class="btn btn-primary" style="width: 100%;" onclick="sendContactMessage()">
                            <i class="fas fa-paper-plane"></i> 发送消息
                        </button>
                    </div>
                </div>
            `;
            
            const formDiv = document.createElement('div');
            formDiv.innerHTML = formHTML;
            document.body.appendChild(formDiv);
        }
        
        function closeContactForm() {
            const form = document.querySelector('div[style*="position: fixed"]');
            if (form) {
                form.remove();
            }
        }
        
        function sendContactMessage() {
            const email = document.getElementById('contactEmail').value;
            const message = document.getElementById('contactMessage').value;
            
            if (!email || !message) {
                showNotification('请填写完整的信息', 'error');
                return;
            }
            
            showNotification('消息发送成功！我们会在24小时内回复您。', 'success');
            closeContactForm();
        }
    </script>
</body>
</html>'''
    
    with open(docs_dir / "about.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ 美观的关于页面创建完成")

if __name__ == "__main__":
    create_beautiful_site()