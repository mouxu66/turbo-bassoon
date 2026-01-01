import re

# 要添加的路由代码
routes_code = '''
# ========== 静态页面路由 (由 mouxu 添加) ==========
@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@app.route('/analysis')
def analysis():
    """数据分析页面"""
    return render_template('analysis.html')

@app.route('/items')
def items():
    """装备数据库页面"""
    return render_template('items.html')

@app.route('/upload')
def upload():
    """数据上传页面"""
    return render_template('upload.html')
'''

with open('app.py', 'r') as f:
    content = f.read()

# 找到最后一个路由定义的位置（通常以 @app.route 或 def 开头）
# 简单策略：在文件末尾的 if __name__ == '__main__': 之前插入
if 'if __name__ == "__main__":' in content:
    parts = content.split('if __name__ == "__main__":', 1)
    new_content = parts[0] + routes_code + '\n\nif __name__ == "__main__":' + parts[1]
else:
    # 如果找不到，直接添加到文件末尾
    new_content = content + '\n\n' + routes_code

with open('app.py', 'w') as f:
    f.write(new_content)

print("✅ 已成功添加4个页面路由：")
print("   /about     /analysis     /items     /upload")
print("⚠️ 请重载Web应用使更改生效！")
