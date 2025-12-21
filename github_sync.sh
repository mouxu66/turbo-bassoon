#!/bin/bash
cd /home/mouxu
python3 generate_static.py
git add .
git commit -m "更新: $(date)"
git push origin main
echo "✅ 同步完成！"
