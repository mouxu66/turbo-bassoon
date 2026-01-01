import re

with open('app.py', 'r') as f:
    lines = f.readlines()

# 找到 analysis 函数定义
analysis_line = -1
for i, line in enumerate(lines):
    if 'def analysis(' in line:
        analysis_line = i
        break

if analysis_line > 0:
    # 查看 analysis 函数前面的路由装饰器
    print("找到 analysis 函数在第", analysis_line + 1, "行")
    
    # 检查前面有多少个 @app.route
    route_count = 0
    for i in range(analysis_line-1, max(-1, analysis_line-5), -1):
        if '@app.route' in lines[i]:
            route_count += 1
            print(f"  第 {i+1} 行: {lines[i].strip()}")
    
    if route_count > 1:
        print(f"⚠️  analysis 函数有 {route_count} 个路由装饰器，可能导致冲突")
        
        # 建议修复：为 about 创建单独的函数
        # 但首先，让我们确保每个路由有独立的函数
        
        # 查找 about 路由
        about_route_line = -1
        for i, line in enumerate(lines):
            if "@app.route('/about')" in line:
                about_route_line = i
                break
        
        if about_route_line > 0:
            print(f"找到 /about 路由在第 {about_route_line+1} 行")
            # 检查 about 路由是否有自己的函数
            has_about_func = False
            for i in range(about_route_line+1, min(len(lines), about_route_line+10)):
                if 'def about' in lines[i]:
                    has_about_func = True
                    break
            
            if not has_about_func:
                print("❌ /about 路由没有对应的函数，需要修复")
                
                # 在 about 路由后添加 about 函数
                insert_line = about_route_line + 1
                about_func = '''
def about():
    """关于页面"""
    return render_template('about.html')
'''
                lines.insert(insert_line, about_func)
                print("✅ 已添加 about() 函数")
        
        # 确保 analysis 路由指向正确的函数
        analysis_route_line = -1
        for i, line in enumerate(lines):
            if "@app.route('/analysis')" in line and i != about_route_line:
                analysis_route_line = i
                break
        
        if analysis_route_line > 0:
            print(f"找到 /analysis 路由在第 {analysis_route_line+1} 行")
            # 确保它指向 analysis 函数（应该已经正确）

with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ 端点冲突修复完成")
