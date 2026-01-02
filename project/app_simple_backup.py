
# ========== GitHub开源项目模块 ==========
import requests
from datetime import datetime

class GitHubOpenSource:
    """GitHub开源项目展示"""
    
    # 精选的LOL相关开源项目
    CURATED_PROJECTS = [
        {
            "name": "riotwatcher",
            "owner": "pseudonym117",
            "description": "Python包装器 for Riot Games API",
            "language": "Python",
            "stars": "1.2k+",
            "url": "https://github.com/pseudonym117/Riot-Watcher"
        },
        {
            "name": "cassiopeia",
            "owner": "meraki-analytics",
            "description": "Python League of Legends API包装器",
            "language": "Python",
            "stars": "500+",
            "url": "https://github.com/meraki-analytics/cassiopeia"
        },
        {
            "name": "lol-js",
            "owner": "Pupix",
            "description": "League of Legends API的JavaScript客户端",
            "language": "JavaScript",
            "stars": "300+",
            "url": "https://github.com/Pupix/lol-js"
        },
        {
            "name": "lolcat",
            "owner": "mrtolkien",
            "description": "命令行版League of Legends数据",
            "language": "Go",
            "stars": "200+",
            "url": "https://github.com/mrtolkien/lolcat"
        },
        {
            "name": "lol-data",
            "owner": "Pupix",
            "description": "League of Legends静态数据",
            "language": "JavaScript",
            "stars": "100+",
            "url": "https://github.com/Pupix/lol-data"
        },
        {
            "name": "league-stats",
            "owner": "vihanb",
            "description": "LoL玩家数据统计",
            "language": "JavaScript",
            "stars": "150+",
            "url": "https://github.com/vihanb/league-stats"
        }
    ]
    
    @staticmethod
    def get_curated_projects():
        """获取精选开源项目列表"""
        return GitHubOpenSource.CURATED_PROJECTS
    
    @staticmethod
    def search_github_repos(query="league of legends", limit=10):
        """搜索GitHub上的LOL相关项目（演示用）"""
        # 注意：实际需要GitHub API token，这里用模拟数据
        return [
            {
                "name": "lol-analysis-tool",
                "full_name": "example/lol-analysis-tool",
                "description": "League of Legends match analysis tool",
                "html_url": "https://github.com/example/lol-analysis-tool",
                "stargazers_count": 150,
                "language": "Python",
                "updated_at": "2024-12-01T00:00:00Z"
            },
            {
                "name": "lol-dashboard",
                "full_name": "example/lol-dashboard",
                "description": "Real-time LoL match dashboard",
                "html_url": "https://github.com/example/lol-dashboard",
                "stargazers_count": 89,
                "language": "JavaScript",
                "updated_at": "2024-11-15T00:00:00Z"
            }
        ]

# 创建实例
github_client = GitHubOpenSource()

# ========== GitHub相关路由 ==========
@app.route('/github')
def github_projects():
    """GitHub开源项目展示页面"""
    projects = github_client.get_curated_projects()
    
    return render_template('github_projects.html',
                         projects=projects,
                         count=len(projects),
                         timestamp=datetime.now().isoformat())

@app.route('/api/github/projects')
def api_github_projects():
    """GitHub项目API"""
    projects = github_client.get_curated_projects()
    
    return jsonify({
        "success": True,
        "source": "curated_demo_data",
        "note": "这是精选项目列表，实际GitHub API需要token",
        "projects": projects,
        "count": len(projects),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/github/search/<query>')
def api_github_search(query):
    """GitHub搜索API（演示）"""
    results = github_client.search_github_repos(query)
    
    return jsonify({
        "success": True,
        "query": query,
        "note": "演示数据 - 实际搜索需要GitHub API token",
        "results": results,
        "count": len(results)
    })

@app.route('/github/how-to-use')
def github_how_to_use():
    """如何使用GitHub开源项目指南"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>如何使用GitHub开源项目 - LoL数据分析</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }
            h1, h2 { color: #24292e; }
            .card { background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 20px; margin: 20px 0; }
            .step { background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #0366d6; }
            code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
            .language-badge { display: inline-block; padding: 4px 8px; background: #e1e4e8; border-radius: 3px; font-size: 12px; margin: 0 5px; }
        </style>
    </head>
    <body>
        <h1>如何使用GitHub上的开源LoL项目</h1>
        
        <div class="card">
            <h2>🎯 为什么使用开源项目？</h2>
            <ul>
                <li><strong>节省时间</strong>: 避免重复造轮子</li>
                <li><strong>学习最佳实践</strong>: 查看优秀代码</li>
                <li><strong>社区支持</strong>: 有问题可以提issue</li>
                <li><strong>持续更新</strong>: 项目会随着游戏更新</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>🚀 快速开始步骤</h2>
            
            <div class="step">
                <h3>步骤1: 寻找合适项目</h3>
                <p>在GitHub搜索: <code>league of legends api</code>、<code>lol数据分析</code>、<code>riot api wrapper</code></p>
                <p>关注指标: Stars数、最近更新、文档完整性</p>
            </div>
            
            <div class="step">
                <h3>步骤2: 安装使用</h3>
                <p><strong>Python项目 (riotwatcher)</strong>:</p>
                <code>pip install riotwatcher</code>
                <pre><code>from riotwatcher import LolWatcher
watcher = LolWatcher(api_key='你的密钥')
summoner = watcher.summoner.by_name('na1', '玩家名')</code></pre>
            </div>
            
            <div class="step">
                <h3>步骤3: 集成到你的项目</h3>
                <p>参考项目的README和examples目录</p>
                <p>注意API速率限制和错误处理</p>
            </div>
            
            <div class="step">
                <h3>步骤4: 贡献和反馈</h3>
                <p>发现问题可以提交issue</p>
                <p>有改进可以提交pull request</p>
                <p>给项目点个⭐支持作者</p>
            </div>
        </div>
        
        <div class="card">
            <h2>🔍 推荐的搜索关键词</h2>
            <p>
                <span class="language-badge">riot api</span>
                <span class="language-badge">league of legends</span>
                <span class="language-badge">lol data analysis</span>
                <span class="language-badge">match analysis</span>
                <span class="language-badge">champion statistics</span>
                <span class="language-badge">esports data</span>
            </p>
        </div>
        
        <div class="card">
            <h2>⚠️ 注意事项</h2>
            <ul>
                <li>检查许可证（MIT、Apache 2.0等）</li>
                <li>遵守Riot Games API使用条款</li>
                <li>注意项目维护状态（最近更新时间）</li>
                <li>测试后再用于生产环境</li>
            </ul>
        </div>
        
        <p><a href="/github">查看精选开源项目</a> | <a href="/">返回首页</a></p>
    </body>
    </html>
    '''
