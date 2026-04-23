import os
import re
from docx import Document
from docxcompose.composer import Composer

# ================== 配置区（请修改为你的实际路径）==================
# Δ提示：路径与 organize_ocr_results.py 中的 OUTPUT_DIR 相同。
BASE_OUTPUT_DIR = r"请在这里输入 要存放生成结果的文件夹 的绝对路径"

def extract_page_number(filename):
    """从文件名中提取页码，例如 'xxx_page_1.docx' 返回 1"""
    match = re.search(r"_page_(\d+)", filename)
    return int(match.group(1)) if match else 0

def merge_docx_in_folder(folder_path):
    """合并指定文件夹内的所有 DOCX 文件"""
    docx_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]
    if not docx_files:
        return
    
    # 按页码排序
    docx_files.sort(key=extract_page_number)
    
    # 使用第一个文档作为基础
    master_doc = Document(os.path.join(folder_path, docx_files[0]))
    composer = Composer(master_doc)
    
    # 追加后续文档
    for docx_file in docx_files[1:]:
        doc = Document(os.path.join(folder_path, docx_file))
        composer.append(doc)
    
    # 保存合并后的文档（以文件夹名命名）
    pdf_name = os.path.basename(folder_path)
    merged_path = os.path.join(folder_path, f"{pdf_name}_完整版.docx")
    composer.save(merged_path)
    print(f"✅ 已合并: {merged_path}")

def main():
    # 遍历 BASE_OUTPUT_DIR 下的所有子文件夹
    for item in os.listdir(BASE_OUTPUT_DIR):
        folder_path = os.path.join(BASE_OUTPUT_DIR, item)
        if os.path.isdir(folder_path) and item != "_unclassified":
            merge_docx_in_folder(folder_path)

if __name__ == "__main__":
    # 如果没有安装 docxcompose，先安装：pip install docxcompose
    try:
        from docxcompose.composer import Composer
    except ImportError:
        print("❌ 请先安装 docxcompose: pip install docxcompose")
        exit(1)
    main()