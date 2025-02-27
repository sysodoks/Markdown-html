import os
import re
import shutil
import argparse
import markdown
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            max-width: 800px;
            margin: 20px auto;
            padding: 0 20px;
            line-height: 1.6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""

def process_images(md_content, md_path, output_dir):
    """处理图片引用并保持原始路径结构"""
    # 获取Markdown文件所在目录
    md_dir = os.path.dirname(md_path)
    
    # 匹配所有图片标记
    img_pattern = re.compile(r'!$$.*?$$$(.*?)$')
    images = set(img_pattern.findall(md_content))
    
    for img_rel_path in images:
        # 跳过网络图片
        if img_rel_path.startswith(('http://', 'https://')):
            continue
            
        # 构建原始图片绝对路径
        src_img_path = os.path.normpath(os.path.join(md_dir, img_rel_path))
        
        if os.path.exists(src_img_path):
            # 构建目标图片路径（保持原始相对路径结构）
            dest_img_path = os.path.join(output_dir, img_rel_path)
            
            # 创建目标目录并复制图片
            os.makedirs(os.path.dirname(dest_img_path), exist_ok=True)
            shutil.copy2(src_img_path, dest_img_path)
            print(f"Copied image: {src_img_path} -> {dest_img_path}")

def convert_md_to_html(md_content, md_path, html_path):
    """转换Markdown并保持图片相对路径"""
    # 计算从HTML文件到图片的相对路径
    html_dir = os.path.dirname(html_path)
    md_dir = os.path.dirname(md_path)
    
    def adjust_path(match):
        img_path = match.group(1)
        if img_path.startswith(('http://', 'https://')):
            return match.group(0)
            
        abs_img_path = os.path.normpath(os.path.join(md_dir, img_path))
        rel_path = os.path.relpath(abs_img_path, html_dir)
        return f'src="{rel_path}"'

    # 转换Markdown为HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    # 修正图片路径
    html_content = re.sub(
        r'src="(.*?)"',
        adjust_path,
        html_content
    )
    
    return HTML_TEMPLATE.format(
        title=Path(md_path).stem,
        content=html_content
    )

def process_directory(input_dir, output_dir):
    """处理目录并保持原始结构"""
    for root, dirs, files in os.walk(input_dir):
        # 创建对应的输出目录
        rel_path = os.path.relpath(root, input_dir)
        dest_root = os.path.join(output_dir, rel_path)
        os.makedirs(dest_root, exist_ok=True)

        for file in files:
            src_path = os.path.join(root, file)
            
            if file.endswith('.md'):
                # 处理Markdown文件
                dest_path = os.path.join(dest_root, f"{Path(file).stem}.html")
                
                try:
                    with open(src_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    
                    # 先处理图片
                    process_images(md_content, src_path, output_dir)
                    
                    # 转换内容
                    html_content = convert_md_to_html(md_content, src_path, dest_path)
                    
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"Converted: {src_path} -> {dest_path}")
                
                except Exception as e:
                    print(f"Error processing {src_path}: {str(e)}")
            
            elif not file.endswith('.html'):
                # 直接复制其他文件
                dest_path = os.path.join(dest_root, file)
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown转换工具')
    parser.add_argument('-i', '--input', required=True, help='输入目录路径')
    parser.add_argument('-o', '--output', default='dist', help='输出目录路径')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print(f"开始转换: {args.input} => {args.output}")
    process_directory(args.input, args.output)
    print("转换完成！")