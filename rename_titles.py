# -*- coding: utf-8 -*-
"""批量重命名文件标题中的敏感词"""
import os
import glob

# 标题敏感词替换映射
TITLE_REPLACEMENTS = {
    "贵人": "大佬",
    "高人": "大佬",
    "高层": "大佬",
    "福报": "回报",
    "天选": "认可",
    "好运": "吉祥"
}

# 目标文件夹
folder_path = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案"

# 查找所有txt文件
txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

print(f"找到 {len(txt_files)} 个txt文件")
print("=" * 60)

renamed_count = 0

for file_path in txt_files:
    file_name = os.path.basename(file_path)
    new_name = file_name

    # 替换标题中的敏感词
    replaced_words = []
    for sensitive, replacement in TITLE_REPLACEMENTS.items():
        if sensitive in new_name:
            count = new_name.count(sensitive)
            new_name = new_name.replace(sensitive, replacement)
            replaced_words.append(f"{sensitive}->{replacement}({count}次)")

    # 如果有修改，重命名文件
    if new_name != file_name:
        new_path = os.path.join(folder_path, new_name)
        os.rename(file_path, new_path)
        renamed_count += 1

        print(f"\n[重命名]")
        print(f"  原名: {file_name}")
        print(f"  新名: {new_name}")
        print(f"  替换: {', '.join(replaced_words)}")

print("\n" + "=" * 60)
print(f"处理完成！")
print(f"  检查文件: {len(txt_files)} 个")
print(f"  重命名文件: {renamed_count} 个")
