# 英雄联盟数据分析网站

一个基于Flask的英雄联盟装备与比赛数据分析平台。

## 在线访问
- PythonAnywhere: https://mouxu.pythonanywhere.com
- GitHub Pages: https://mouxu66.github.io/turbo-bassoon

## 功能特点
- 装备数据查询
- 比赛数据分析
- CSV文件上传
- 数据可视化

## 技术栈
- Flask后端
- SQLite数据库
- Bootstrap前端

## 本地运行
```bash
pip install -r requirements.txt
python app.py

# ========== 1. 连接GitHub ==========
cd /home/mouxu
git init
git config user.email "你的邮箱"
git config user.name "mouxu66"
git remote add origin https://github.com/mouxu66/turbo-bassoon.git

# ========== 2. 创建必要文件 ==========
# 创建.gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.db
instance/
uploads/
*.log
