with open('app.py', 'r') as f:
    lines = f.readlines()

# 查找最后一个路由函数结束的位置（寻找一个没有@app.route的行）
insert_line = 560  # 在第565行的upload路由之前插入
for i in range(550, 570):
    if '@app.route' in lines[i] and '/upload' in lines[i]:
        insert_line = i
        break

# 要插入的代码
new_routes = '''
@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@app.route('/analysis')
def analysis():
    """数据分析页面"""
    return render_template('analysis.html')
'''

# 插入新路由
lines.insert(insert_line, new_routes)

with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ 已添加 /about 和 /analysis 路由函数")
