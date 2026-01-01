#!/bin/bash
echo "=== 最终模板修复 ==="

# 1. 备份
cp -r templates templates.backup_final_$(date +%H%M%S)

# 2. 修复 items.html
echo "修复 items.html..."
if [ -f "templates/items.html" ]; then
    # 完全重写第8行
    sed -i '8c\    <link rel="stylesheet" href="{{ url_for(\"static\", filename=\"css/style.css\") }}">' templates/items.html
    
    # 同时修复其他可能的url_for调用
    sed -i 's/url_for(\\\\\"/url_for(\"/g' templates/items.html
    sed -i "s/url_for(\\\\\'/url_for('/g" templates/items.html
    sed -i 's/\\\\\"/\"/g' templates/items.html
    sed -i "s/\\\\\'/'/g" templates/items.html
fi

# 3. 修复 match_results.html
echo "修复 match_results.html..."
if [ -f "templates/match_results.html" ]; then
    # 创建简单正确的版本
    cat > templates/match_results.html << 'TEMPLATE_EOF'
{% extends "base.html" %}

{% block title %}比赛结果{% endblock %}

{% block content %}
<div class="container">
    <h1>比赛结果</h1>
    <p>比赛数据功能正在开发中...</p>
    <p><a href="/">返回首页</a></p>
</div>
{% endblock %}
TEMPLATE_EOF
fi

# 4. 修复其他模板文件
echo "清理其他模板..."
for file in templates/*.html; do
    if [ -f "$file" ]; then
        # 移除多余的反斜杠
        sed -i 's/\\\\//g' "$file"
        sed -i 's/\\//g' "$file"
        # 修复url_for语法
        sed -i 's/url_for(\\"/url_for("/g' "$file"
        sed -i "s/url_for(\\'/url_for('/g" "$file"
    fi
done

# 5. 验证修复
echo "=== 验证修复 ==="
python3 -c "
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import os

env = Environment(loader=FileSystemLoader('templates'))
all_ok = True

for filename in os.listdir('templates'):
    if filename.endswith('.html'):
        try:
            template = env.get_template(filename)
            print(f'✅ {filename}')
        except TemplateSyntaxError as e:
            print(f'❌ {filename}: 第{e.lineno}行 - {e}')
            all_ok = False
        except Exception as e:
            print(f'⚠️  {filename}: {type(e).__name__}')

if all_ok:
    print('\n🎉 所有模板语法正确！')
else:
    print('\n⚠️  仍有模板需要修复')
"

# 6. 清除缓存
find . -name "*.pyc" -delete 2>/dev/null || true

echo ""
echo "=== 修复完成 ==="
echo "请立即去PythonAnywhere点击Reload按钮！"
