with open('static/js/main.js', 'r') as f:
    content = f.read()

# 替换updateStats函数中的ID
old_function = '''function updateStats(data) {
    document.getElementById('item-count').textContent = data.itemCount || 0;
    document.getElementById('match-count').textContent = data.matchCount || 0;
    document.getElementById('data-size').textContent = data.totalSize || '0';
}'''

new_function = '''function updateStats(data) {
    // 使用正确的HTML元素ID
    const itemEl = document.getElementById('stat-items');
    const matchEl = document.getElementById('stat-matches');
    const sizeEl = document.getElementById('data-size'); // 这个元素需要添加
    
    if (itemEl) itemEl.textContent = data.itemCount || 0;
    if (matchEl) matchEl.textContent = data.matchCount || 0;
    if (sizeEl) sizeEl.textContent = data.totalSize || '0';
}'''

if old_function in content:
    content = content.replace(old_function, new_function)
    with open('static/js/main.js', 'w') as f:
        f.write(content)
    print("✅ 已修复JS中的元素ID匹配问题")
else:
    print("⚠️  未找到原函数，可能已被修改")
