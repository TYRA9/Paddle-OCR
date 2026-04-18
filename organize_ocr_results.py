import os
import shutil
import glob

# ================== 配置区 ==================
# 这里需要换成自己的路径（前面的小写字母 r 是起到转义的作用）
# CORPORA_DIR : 这是你的语料(PDF 文件) 所存放的路径(用绝对路径，且路径要规范)
# OUTPUT_DIR : 这是你的OCR模型跑完后，存放生成结果的路径(同样用绝对路径)
CORPORA_DIR = r"请在这里输入 语料所在文件夹 的绝对路径"
OUTPUT_DIR = r"请在这里输入 要存放生成结果的文件夹 的绝对路径"

# 需要整理的文件扩展名（增加了 docx 和 tex）
EXTENSIONS = [".md", ".json", ".jpg", ".jpeg", ".png", ".docx", ".tex"]

def get_pdf_basenames(corpora_dir):
    """从 corpora 文件夹读取所有 PDF 的基础名（不含扩展名）"""
    pdf_files = glob.glob(os.path.join(corpora_dir, "*.pdf"))
    return [os.path.splitext(os.path.basename(f))[0] for f in pdf_files]

def organize_files_by_pdf_name(output_dir, pdf_basenames):
    # 收集所有待整理的文件
    all_files = []
    for ext in EXTENSIONS:
        all_files.extend(glob.glob(os.path.join(output_dir, f"*{ext}")))
    
    # 为每个已知 PDF 创建空列表，并准备一个“未分类”组
    pdf_groups = {name: [] for name in pdf_basenames}
    pdf_groups["_unclassified"] = []
    
    for file_path in all_files:
        base_name = os.path.basename(file_path)
        matched = False
        # 按 PDF 基础名匹配：只要文件名以“PDF基础名”开头，就归入该组
        for pdf_name in pdf_basenames:
            if base_name.startswith(pdf_name):
                pdf_groups[pdf_name].append(file_path)
                matched = True
                break
        if not matched:
            pdf_groups["_unclassified"].append(file_path)
    
    # 移动文件到对应子文件夹
    for pdf_name, files in pdf_groups.items():
        if not files:
            continue
        sub_dir = os.path.join(output_dir, pdf_name)
        os.makedirs(sub_dir, exist_ok=True)
        for file_path in files:
            dest = os.path.join(sub_dir, os.path.basename(file_path))
            shutil.move(file_path, dest)
            print(f"移动: {os.path.basename(file_path)} -> {pdf_name}/")

if __name__ == "__main__":
    pdf_names = get_pdf_basenames(CORPORA_DIR)
    print(f"发现 {len(pdf_names)} 个 PDF 基础名")
    organize_files_by_pdf_name(OUTPUT_DIR, pdf_names)
    print("\n✅ 所有文件已按 PDF 归类完毕！")