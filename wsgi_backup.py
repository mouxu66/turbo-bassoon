# /var/www/你的用户名_pythonanywhere_com_wsgi.py
import sys
import os

# ============================================
# 选择要运行的版本
# ============================================

# 选项1: 作业简化版（推荐，避免CPU超额）
RUN_MODE = "SIMPLE"  # SIMPLE 或 FULL

# 选项2: 完整功能版（谨慎使用，可能CPU超额）
# RUN_MODE = "FULL"

# ============================================
# 路径配置
# ============================================

# 你的项目路径
project_path = '/home/你的用户名/你的项目文件夹名'

# 确保路径在系统路径中
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# 设置环境变量
os.environ['PROJECT_ROOT'] = project_path

# ============================================
# 根据模式加载对应的应用
# ============================================

try:
    if RUN_MODE == "SIMPLE":
        print(f"🎯 运行模式: 作业简化版 (SIMPLE)")
        print(f"📁 项目路径: {project_path}")
        
        # 导入简化版应用
        from app_simple import app
        
        # 设置Flask配置
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        # 应用对象
        application = app
        
        print("✅ 简化版应用加载成功")
        print("📝 特性: 演示数据 + 基础API + 低CPU消耗")
        
    elif RUN_MODE == "FULL":
        print(f"🎯 运行模式: 完整功能版 (FULL)")
        print(f"📁 项目路径: {project_path}")
        print("⚠️  警告: 完整版可能消耗较多CPU")
        
        # 导入完整版应用
        from app import app as full_app
        
        # 配置完整版
        full_app.config['ENV'] = 'production'
        full_app.config['DEBUG'] = False
        full_app.config['TESTING'] = False
        
        # 应用对象
        application = full_app
        
        print("✅ 完整版应用加载成功")
        print("📝 特性: 实时API + 数据分析 + 完整功能")
        
    else:
        raise ValueError(f"未知的运行模式: {RUN_MODE}")
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print(f"📁 当前目录: {os.getcwd()}")
    print(f"📁 sys.path: {sys.path}")
    
    # 创建错误应用
    from flask import Flask
    error_app = Flask(__name__)
    
    @error_app.route('/')
    def error_page():
        return f"""
        <h1>应用加载错误</h1>
        <p>错误: {str(e)}</p>
        <p>请检查:</p>
        <ol>
            <li>项目路径: {project_path}</li>
            <li>文件是否存在: app_simple.py 或 app.py</li>
            <li>WSGI配置是否正确</li>
        </ol>
        <p>运行模式: {RUN_MODE}</p>
        """
    
    application = error_app

except Exception as e:
    print(f"❌ 其他错误: {e}")
    
    # 创建错误应用
    from flask import Flask
    error_app = Flask(__name__)
    
    @error_app.route('/')
    def error_page():
        return f"""
        <h1>应用配置错误</h1>
        <p>错误: {str(e)}</p>
        <p>请联系管理员检查WSGI配置</p>
        """
    
    application = error_app

# ============================================
# 日志信息
# ============================================
print("=" * 50)
print("WSGI配置加载完成")
print(f"模式: {RUN_MODE}")
print(f"时间: {__import__('datetime').datetime.now()}")
print("=" * 50)