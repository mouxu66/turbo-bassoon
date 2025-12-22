#!/bin/bash

echo "🚀 一键部署完整网站"
echo "======================"

cd /home/mouxu

echo "1. 生成完整网站..."
python3 generate_full_site.py

echo ""
echo "2. 查看生成的文件..."
find docs/ -type f -name "*.html" | head -10

echo ""
echo "3. 推送到GitHub..."
git add docs/
git commit -m "完整部署: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo ""
echo "✅ 部署完成！"
echo ""
echo "📱 访问你的网站："
echo "   🌐 https://mouxu66.github.io/turbo-bassoon"
echo "   ⚡ https://mouxu.pythonanywhere.com"
echo ""
echo "📁 网站包含："
echo "   • 首页（数据统计）"
echo "   • 装备数据库（50+装备）"
echo "   • 比赛分析（图表可视化）"
echo "   • 数据文件下载"
echo "   • 关于页面"
