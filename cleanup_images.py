import os
import glob

# ================== 配置区（请修改为你的实际路径）==================
# Δ提示：路径与 organize_ocr_results.py 中的 OUTPUT_DIR 相同。
BASE_OUTPUT_DIR = r"请在这里输入 要存放生成结果的文件夹 的绝对路径"

# 需要删除的图片扩展名（可按需增删）
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

def find_all_images(base_dir):
    """递归查找所有图片文件，返回完整路径列表"""
    image_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(IMAGE_EXTS):
                image_files.append(os.path.join(root, file))
    return image_files

def main():
    print(f"正在扫描目录: {BASE_OUTPUT_DIR}")
    images = find_all_images(BASE_OUTPUT_DIR)
    
    if not images:
        print("✅ 没有找到任何图片文件，无需清理。")
        return
    
    print(f"\n发现 {len(images)} 个图片文件：")
    for img in images[:10]:  # 最多显示前10个，避免刷屏
        print(f"  - {os.path.relpath(img, BASE_OUTPUT_DIR)}")
    if len(images) > 10:
        print(f"  ... 还有 {len(images) - 10} 个文件")
    
    # 请求用户确认
    confirm = input("\n是否永久删除这些图片？(y/n): ").strip().lower()
    if confirm != 'y':
        print("操作已取消。")
        return
    
    # 执行删除
    deleted_count = 0
    for img in images:
        try:
            os.remove(img)
            deleted_count += 1
        except Exception as e:
            print(f"删除失败: {img} - {e}")
    
    print(f"\n✅ 已删除 {deleted_count} 个图片文件。")

if __name__ == "__main__":
    main()