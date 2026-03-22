"""
移动标题字数超过46个字的Word文档
源文件夹: D:\A文章work\阿木木
目标文件夹: D:\A文章work\国学故事
"""

import os
import shutil

# 配置路径
source_folder = r"D:\A文章work\阿木木"
target_folder = r"D:\A文章work\国学故事"

# 标题字数阈值
TITLE_LENGTH_THRESHOLD = 46

def main():
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"已创建目标文件夹: {target_folder}")

    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误: 源文件夹不存在 - {source_folder}")
        return

    moved_count = 0
    skipped_count = 0

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        # 只处理Word文档
        if not filename.lower().endswith(('.doc', '.docx')):
            continue

        # 获取文件名（不含扩展名）作为标题
        title = os.path.splitext(filename)[0]
        title_length = len(title)

        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)

        # 检查标题字数是否超过阈值
        if title_length > TITLE_LENGTH_THRESHOLD:
            try:
                shutil.move(source_path, target_path)
                print(f"已移动: {filename} (标题{title_length}字)")
                moved_count += 1
            except Exception as e:
                print(f"移动失败: {filename} - {e}")
        else:
            skipped_count += 1

    print(f"\n处理完成!")
    print(f"移动文件数: {moved_count}")
    print(f"保留文件数: {skipped_count}")

if __name__ == "__main__":
    main()
