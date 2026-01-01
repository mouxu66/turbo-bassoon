import re

def fix_items_html():
    """修复items.html第8行"""
    with open('templates/items.html', 'r') as f:
        lines = f.readlines()
    
    # 第8行（索引7）
    if len(lines) > 7:
        line = lines[7]
        print(f"items.html第8行原内容: {repr(line)}")
        
        # 修复url_for语法：确保有逗号分隔参数
        if 'url_for' in line and 'static' in line:
            # 将 url_for('static' filename=...) 改为 url_for('static', filename=...)
            line = re.sub(r"url_for\('static'\s+filename=", "url_for('static', filename=", line)
            line = re.sub(r'url_for\("static"\s+filename=', 'url_for("static", filename=', line)
            lines[7] = line
            print(f"修复后: {repr(line)}")
    
    with open('templates/items.html', 'w') as f:
        f.writelines(lines)
    print("✅ items.html 修复完成")

def fix_match_results_html():
    """修复match_results.html重复block"""
    with open('templates/match_results.html', 'r') as f:
        content = f.read()
    
    # 统计block content出现次数
    blocks = re.findall(r'\{%\s*block\s+content\s*%\}', content)
    if len(blocks) > 1:
        print(f"发现 {len(blocks)} 个重复的block content")
        # 删除多余的block，只保留第一个
        content = re.sub(r'\{%\s*block\s+content\s*%\}(.*?)\{%\s*endblock\s*%\}', 
                        r'{% block content %}\1{% endblock %}', 
                        content, flags=re.DOTALL)
    
    with open('templates/match_results.html', 'w') as f:
        f.write(content)
    print("✅ match_results.html 修复完成")

def check_all_templates():
    """检查所有模板语法"""
    from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
    
    env = Environment(loader=FileSystemLoader('templates'))
    
    for filename in ['items.html', 'match_results.html', 'index.html']:
        try:
            template = env.get_template(filename)
            print(f"✅ {filename}: 语法正确")
        except TemplateSyntaxError as e:
            print(f"❌ {filename}: 第{e.lineno}行 - {e}")
        except Exception as e:
            print(f"⚠️  {filename}: {type(e).__name__}")

if __name__ == '__main__':
    print("开始修复模板错误...")
    fix_items_html()
    fix_match_results_html()
    print("\n修复完成，检查结果:")
    check_all_templates()
