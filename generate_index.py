import os
import re
from pathlib import Path

def generate_index(input_dirs, output_file="index.html"):
    """生成带目录导航的索引页（数字排序版）"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>文档导航</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 0 20px;
            line-height: 1.6;
        }}
        .folder {{
            margin: 15px 0;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 4px;
        }}
        .folder-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        details > summary {{
            list-style: none;
            cursor: pointer;
        }}
        details > summary::-webkit-details-marker {{
            display: none;
        }}
        details summary:before {{
            content: "📁";
            margin-right: 6px;
        }}
        details[open] summary:before {{
            content: "📂";
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>文档导航</h1>
'''

    # 对输入目录进行排序
    input_dirs = sorted(input_dirs, key=lambda x: os.path.basename(x.rstrip('/')).lower())
    
    for input_dir in input_dirs:
        dir_name = os.path.basename(input_dir.rstrip('/'))
        html += f'    <div class="folder">\n'
        html += f'        <div class="folder-title">📁 {dir_name}</div>\n'
        html += '        <ul>\n'
        
        # 生成排序后的目录树
        html += generate_sorted_tree(input_dir, input_dir)
        
        html += '        </ul>\n'
        html += '    </div>\n'

    html += '''</body>
</html>'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"导航页已生成：{os.path.abspath(output_file)}")

def extract_number(name):
    """提取文件名开头的数字"""
    match = re.match(r'^(\d+)', name)
    return int(match.group(1)) if match else float('inf')

def generate_sorted_tree(root_dir, base_dir, current_dir="", depth=0):
    """递归生成按数字排序的目录结构"""
    items = []
    current_path = os.path.join(root_dir, current_dir)
    
    # 获取并排序目录内容
    try:
        dir_entries = os.listdir(current_path)
    except Exception as e:
        return f"<li>⚠️ 无法读取目录 {current_path}: {str(e)}</li>"
    
    # 先处理文件夹，后处理文件
    dirs = [d for d in dir_entries if os.path.isdir(os.path.join(current_path, d))]
    files = [f for f in dir_entries if f.endswith(".html") and f != "index.html"]
    
    # 按数字顺序排序文件夹
    dirs = sorted(dirs, key=lambda x: extract_number(x))
    
    # 生成文件夹结构
    for dir_name in dirs:
        rel_path = os.path.join(current_dir, dir_name)
        sub_items = generate_sorted_tree(root_dir, base_dir, rel_path, depth+1)
        items.append(f'''
{'    ' * (depth+2)}<li>
{'    ' * (depth+3)}<details {'open' if depth < 2 else ''}>
{'    ' * (depth+3)}    <summary>{dir_name}/</summary>
{'    ' * (depth+4)}<ul>
{sub_items}
{'    ' * (depth+4)}</ul>
{'    ' * (depth+3)}</details>
{'    ' * (depth+2)}</li>
''')
    
    # 按数字顺序排序文件
    files = sorted(files, key=lambda x: extract_number(x))
    
    # 生成文件列表
    for file_name in files:
        file_path = os.path.join(root_dir, current_dir, file_name)
        relative_link = os.path.relpath(file_path, base_dir)
        items.append(f'''
{'    ' * (depth+2)}<li>
{'    ' * (depth+3)}<a href="./{os.path.basename(base_dir)}/{relative_link}">{file_name}</a>
{'    ' * (depth+2)}</li>
''')
    
    return '\n'.join(items)
def convert_md_to_html(md_content, input_path, output_path):
    """将Markdown内容转换为HTML并处理图片资源"""
    # 创建输出目录
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # 提取并复制图片资源
    image_paths = extract_image_paths(md_content, input_path)
    copy_images(image_paths, output_dir)
    
    # 转换Markdown为HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    # 修正图片路径
    html_content = adjust_image_paths(html_content, input_path, output_path)
    
    return HTML_TEMPLATE.format(
        title=Path(input_path).stem,
        content=html_content
    )

def extract_image_paths(md_content, md_file_path):
    """从Markdown内容中提取所有图片路径"""
    img_pattern = r'!$$.*?$$$(.*?)$'
    matches = re.findall(img_pattern, md_content)
    
    # 获取绝对路径
    base_dir = os.path.dirname(md_file_path)
    return [os.path.normpath(os.path.join(base_dir, m)) for m in matches]

def copy_images(image_paths, output_dir):
    """复制图片到输出目录"""
    for src_path in image_paths:
        if os.path.exists(src_path):
            # 保持相对目录结构
            rel_path = os.path.relpath(src_path, start=os.path.dirname(src_path))
            dest_path = os.path.join(output_dir, rel_path)
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)

def adjust_image_paths(html_content, input_path, output_path):
    """修正HTML中的图片路径"""
    md_dir = os.path.dirname(input_path)
    html_dir = os.path.dirname(output_path)
    
    # 计算相对路径
    rel_path = os.path.relpath(md_dir, html_dir)
    
    # 替换图片路径
    return re.sub(
        r'src="(.*?)"',
        lambda m: f'src="{os.path.join(rel_path, m.group(1))}"' if not m.group(1).startswith(('http://', 'https://')) else m.group(0),
        html_content
    )

# 原process_directory函数需要增加图片处理
def process_directory(input_dir, output_dir):
    """递归处理目录（新增图片处理）"""
    for root, dirs, files in os.walk(input_dir):
        # 在输出目录创建对应的子目录
        relative_path = os.path.relpath(root, input_dir)
        dest_dir = os.path.join(output_dir, relative_path)
        os.makedirs(dest_dir, exist_ok=True)

        # 处理每个Markdown文件
        for file in files:
            if file.endswith('.md'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(
                    dest_dir,
                    f"{os.path.splitext(file)[0]}.html"
                )

                try:
                    # 读取并转换文件
                    with open(input_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    
                    html_content = convert_md_to_html(md_content, input_path, output_path)
                    
                    # 写入输出文件
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"Converted: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")

            # 新增：直接复制非Markdown文件
            elif not file.endswith(('.html', '.md')):
                src = os.path.join(root, file)
                dest = os.path.join(dest_dir, file)
                shutil.copy2(src, dest)
                print(f"Copied: {src} -> {dest}")

# HTML模板需要添加基本样式（可选）
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* 添加图片样式 */
        img {{
            max-width: 100%;
            height: auto;
            margin: 10px 0;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        /* 原有样式保持不变 */
    </style>
</head>
<body>
{content}
</body>
</html>
"""
if __name__ == "__main__":
    # 自动检测输出目录
    output_dirs = [d for d in ["dist", "dist2"] if os.path.exists(d)]
    
    if not output_dirs:
        print("错误：未找到任何输出目录")
        exit(1)
        
    generate_index(output_dirs, "index.html")