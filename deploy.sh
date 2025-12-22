#!/bin/bash
echo "开始部署..."
git add .
read -p "请输入本次提交的说明: " commit_msg
git commit -m "$commit_msg"
git push origin main
echo "代码已推送到GitHub。"
echo "请到PythonAnywhere的Web界面手动重载应用。"

