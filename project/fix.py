# 读取整个文件
with open('templates/index.html', 'r') as f:
    lines = f.readlines()

# 直接修改第7、8、9行（注意：列表索引从0开始）
lines[6] = '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/style.css\') }}">\n'
lines[7] = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'
lines[8] = '    <script src="{{ url_for(\'static\', filename=\'js/main.js\') }}" defer></script>\n'

# 写回文件
with open('templates/index.html', 'w') as f:
    f.writelines(lines)

print("修复完成！")
