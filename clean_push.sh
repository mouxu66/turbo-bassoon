#!/bin/bash

echo "🧹 清理并推送..."

cd /home/mouxu

# 1. 删除包含Token的文件
echo "删除包含Token的文件..."
rm -f push_with_token.sh

# 2. 从Git历史中移除
echo "从Git历史中移除敏感文件..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch push_with_token.sh" \
  --prune-empty --tag-name-filter cat -- --all

# 3. 清理Git
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now

# 4. 设置新的远程（不在脚本中保存Token）
echo "请输入GitHub Token（不会保存）："
read -s token
echo

git remote remove origin
git remote add origin "https://${token}@github.com/mouxu66/turbo-bassoon.git"

# 5. 强制推送
git push -f origin main

echo "✅ 清理完成！"
