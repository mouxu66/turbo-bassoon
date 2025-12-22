#!/bin/bash

echo "🔄 自动更新网站..."
cd /home/mouxu

# 1. 生成最新网站
python3 generate_full_site.py

# 2. 检查更改
if git status --porcelain | grep -q docs; then
    echo "检测到网站更新，提交到GitHub..."
    git add docs/
    git commit -m "自动更新: $(date '+%Y-%m-%d %H:%M')"
    git push origin main
    echo "✅ 更新已推送，GitHub Pages将自动部署"
else
    echo "📭 没有检测到更改"
fi

echo "🌐 网站: https://mouxu66.github.io/turbo-bassoon"
