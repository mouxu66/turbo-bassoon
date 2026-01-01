with open('templates/index.html', 'r') as f:
    content = f.read()

# 统计替换前的情况
count_before = content.count('/items.html')
print(f"找到 {count_before} 处 '/items.html' 链接")

# 替换为正确的Flask路由
content = content.replace('href="/items.html"', 'href="/items"')

# 也可以替换为 url_for 语法（更规范）
# content = content.replace('href="/items.html"', 'href="{{ url_for(\\'items_page\\') }}"')

count_after = content.count('/items.html')
changes = count_before - count_after

with open('templates/index.html', 'w') as f:
    f.write(content)

print(f"✅ 已修复 {changes} 处链接")
print("修改后的链接示例:")
print([line for line in content.split('\n') if 'href="/items"' in line][:2])
