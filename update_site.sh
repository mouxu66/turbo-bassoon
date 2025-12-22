#!/bin/bash

echo "🔄 更新GitHub Pages网站..."

cd /home/mouxu

# 更新部署时间
sed -i "s/部署时间: .*/部署时间: $(date)/" docs/index.html

# 提交并推送
git add .
git commit -m "更新时间: $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo ""
echo "✅ 更新完成！"
echo "🌐 网站将在1-2分钟内自动更新"
echo "📱 访问: https://mouxu66.github.io/turbo-bassoon"
