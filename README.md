# Markdown-html
这是一个Markdown转化为html格式到可视化的项目

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

## md2html.py 使用说明

bash
命令
python md2html.py -i <输入目录> [-o <输出目录>]

-i/--input：必填，指定包含Markdown文件的输入目录
-o/--output：可选，指定输出目录（默认为dist）

bash
# 基本用法
python md2html.py -i ./docs

# 指定输出目录
python md2html.py -i ./my_notes -o ./output

## generate_index.py 使用说明

### 功能
生成导航页面，展示所有HTML文件的目录结构

bash
python generate_index.py [-o <输出文件>]

###参数说明
自动检测dist和dist2目录
默认输出到index.html

bash
# 基本用法（自动检测dist目录）
python generate_index.py

# 自定义输出文件
python generate_index.py -o ./docs_index.html


## 四、完整工作流程
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
