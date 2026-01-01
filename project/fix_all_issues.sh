#!/bin/bash
echo "=== 修复所有问题 ==="

# 备份
cp app.py app.py.backup_all

# 1. 删除第548行（有缩进问题的行）
echo "1. 删除有问题的第548行..."
sed -i '548d' app.py

# 2. 检查是否还有其他问题
echo "2. 检查上下文..."
sed -n '545,555p' app.py

# 3. 修复可能的多余空行
echo "3. 清理多余空行..."
sed -i '547,548{/^$/d}' app.py  # 删除547-548行的空行

# 4. 确保代码连贯
echo "4. 检查代码连贯性..."
awk 'NR>=540 && NR<=560 {printf "%3d: %s\n", NR, $0}' app.py

# 5. 测试修复
echo "5. 测试修复..."
if python3 -m py_compile app.py 2>/dev/null; then
    echo "   ✅ 语法检查通过"
    
    if python3 -c "from app import app; print('   ✅ 导入成功')" 2>/dev/null; then
        echo "   ✅ Flask应用导入成功"
        echo ""
        echo "🎉 所有问题已修复！"
    else
        echo "   ❌ 导入失败"
        python3 -c "from app import app" 2>&1 | head -10
    fi
else
    echo "   ❌ 语法错误"
    python3 -m py_compile app.py
fi

# 清除缓存
find . -name "*.pyc" -delete 2>/dev/null || true
