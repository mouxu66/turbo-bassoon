#!/bin/bash

echo "🔑 GitHub Token配置脚本"
echo "========================"

cd /home/mouxu

echo "1. 删除旧的远程连接..."
git remote remove origin

echo ""
echo "2. 请粘贴你的GitHub Token:"
echo "   （访问 https://github.com/settings/tokens 生成）"
read -p "   Token: " github_token

echo ""
echo "3. 设置新的远程地址..."
git remote add origin "https://mouxu66:${github_token}@github.com/mouxu66/turbo-bassoon.git"

echo ""
echo "4. 测试连接..."
git push origin main

echo ""
echo "✅ 完成！如果看到推送成功信息，就配置好了。"
