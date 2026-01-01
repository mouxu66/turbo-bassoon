#!/usr/bin/env python3
import re

with open('templates/index.html', 'r') as f:
    content = f.read()

# 要添加的HTML代码
last_update_html = '''<!-- 最后更新时间显示 -->
<div style="text-align: center; color: #888; margin: 10px 0; font-size: 14px;">
    最后更新: <span id="last-update">正在加载...</span>
</div>'''

search_box_html = '''<!-- 装备搜索框 -->
<div style="max-width: 500px; margin: 20px auto; padding: 0 15px;">
    <input 
        type="text" 
        id="search-item" 
        placeholder="搜索装备名称或属性..." 
        style="width: 100%; padding: 12px 15px; border: 2px solid #4a90e2; border-radius: 25px; font-size: 16px; outline: none;"
    >
</div>'''

# 策略1：在第一个</div>闭合标签后插入（通常在主内容区）
if '</div>' in content:
    # 在第一个主要</div>后添加搜索框和时间
    parts = content.split('</div>', 1)
    new_content = parts[0] + '</div>\n' + last_update_html + '\n' + search_box_html + '\n' + parts[1]
else:
    # 策略2：在<body>标签后直接添加
    new_content = content.replace('<body>', '<body>\n' + last_update_html + '\n' + search_box_html + '\n')

with open('templates/index.html', 'w') as f:
    f.write(new_content)

print("✅ 已自动添加HTML元素！")
print("1. 最后更新时间显示 (id='last-update')")
print("2. 装备搜索框 (id='search-item')")
