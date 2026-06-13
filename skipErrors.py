""" 
skipErrors.py 脚本的核心逻辑流程：
    加载模型（一次）
    ↓
    遍历 corpora 目录下的所有 PDF
    ↓
    对每个 PDF：
    ├─ try:
    │    ├─ 调用 pipeline.predict(pdf) → 得到识别结果
    │    ├─ 保存为 .docx / .md / .json
    │    └─ 打印 "✅ 成功"
    └─ except:
            ├─ 打印 "❌ 失败" + 错误信息
            └─ continue（跳过，进入下一个 PDF）
    ↓
    全部处理完毕，打印成功/失败统计
"""

import os
import glob
from paddleocr import PPStructureV3

os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

# ================== 配置区 ==================
INPUT_DIR = r"请在这里输入 语料所在文件夹 的绝对路径"
OUTPUT_DIR = r"请在这里输入 要存放生成结果的文件夹 的绝对路径"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("正在加载模型...")
pipeline = PPStructureV3(device="gpu")
print("模型加载完成。\n")

pdf_files = glob.glob(os.path.join(INPUT_DIR, "*.pdf"))
total = len(pdf_files)

if total == 0:
    print(f"在 {INPUT_DIR} 中未找到 PDF。")
    exit()

success = fail = 0
for idx, pdf in enumerate(pdf_files, 1):
    name = os.path.basename(pdf)
    print(f"[{idx}/{total}] 正在处理: {name}")
    try:
        results = pipeline.predict(pdf)
        
        # 新版 API：LayoutParsingResultV2 使用 save_all() 保存所有格式
        for res in results:
            # save_all() 会将结果保存为 Markdown、JSON、Word、图片等
            res.save_all(save_path=OUTPUT_DIR)
        
        print("  ✅ 成功")
        success += 1
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        fail += 1
    print("-" * 60)

print(f"\n处理完毕。成功: {success}, 失败: {fail}")