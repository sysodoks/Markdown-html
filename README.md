# Markdown转换工具包使用说明

## 工具组成
1. ​**md2html.py**​ - Markdown批量转换工具
2. ​**generate_index.py**​ - 导航页生成工具

---

## 一、环境准备
1. 安装Python 3.6+
2. 安装依赖库：
```bash
pip install markdown
二、md2html.py 使用说明
功能
将指定目录下的Markdown文件转换为HTML，保留原始目录结构和图片资源

命令格式
bash
python md2html.py -i <输入目录> [-o <输出目录>]
参数说明
-i/--input：必填，指定包含Markdown文件的输入目录

-o/--output：可选，指定输出目录（默认为dist）

使用示例
bash
# 基本用法
python md2html.py -i ./docs

# 指定输出目录
python md2html.py -i ./my_notes -o ./output
转换规则
保留原始目录结构

自动复制所有图片资源（保持原始路径）

支持以下文件处理：

.md → .html

其他文件原样复制

三、generate_index.py 使用说明
功能
生成导航页面，展示所有HTML文件的目录结构

命令格式
bash
python generate_index.py [-o <输出文件>]
参数说明
自动检测dist和dist2目录

默认输出到index.html

使用示例
bash
# 基本用法（自动检测dist目录）
python generate_index.py

# 自定义输出文件
python generate_index.py -o ./docs_index.html
四、完整工作流程
​转换Markdown

bash
python md2html.py -i ./source_docs
​生成导航页

bash
python generate_index.py
​访问结果



打开生成的index.html文件，通过浏览器访问：

markdown
file:///path/to/dist/index.html
五、目录结构示例
转换前
markdown
source_docs/
├─ 1-指南/
│  ├─ 1-快速入门.md
│  └─ images/
│     └─ demo.png
└─ 2-API/
   └─ 参考手册.md
转换后
dist/
├─ 1-指南/
│  ├─ 1-快速入门.html
│  └─ images/
│     └─ demo.png
├─ 2-API/
│  └─ 参考手册.html
└─ index.html
六、注意事项
​路径规范：

建议使用英文路径

避免使用特殊字符（空格、#、%等）

​图片处理：

支持格式：.png、.jpg、.gif、.svg

网络图片保持原链接

本地图片自动保持原始路径结构


