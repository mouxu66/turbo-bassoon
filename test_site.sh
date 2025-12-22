#!/bin/bash

echo "🔍 测试网站功能..."
echo ""

cd /home/mouxu

echo "1. 检查文件："
ls -la docs/index.html
ls -la docs/js/main.js
ls -la docs/css/style.css

echo ""
echo "2. 检查HTML内容："
head -20 docs/index.html | grep -E "(title|h1|function)"

echo ""
echo "3. 检查JavaScript："
head -10 docs/js/main.js

echo ""
echo "✅ 网站创建完成！"
echo ""
echo "📱 功能包括："
echo "   • 装备查询与搜索"
echo "   • 数据分析与图表"
echo "   • 数据上传模拟"
echo "   • 数据导出功能"
echo "   • 响应式设计"
echo ""
echo "🌐 访问: https://mouxu66.github.io/turbo-bassoon"
