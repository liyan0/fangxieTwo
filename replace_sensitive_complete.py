# -*- coding: utf-8 -*-
"""敏感词替换工具 - 完整版"""
import os
import glob
import re

# 标题敏感词替换映射
TITLE_SENSITIVE_WORDS = {
    "贵人": "大佬",
    "高层": "上面那位",
    "福报": "回报",
    "福气": "福泽",
    "好运": "吉祥"
}

# 内容敏感词替换映射
CONTENT_SENSITIVE_WORDS = {
    "点赞": "支持",
    "评论": "交流",
    "留言": "互动",
    "好运": "吉祥",
    "翻身": "翻盘",
    "福报": "回报",
    "福气": "祥瑞",
    "小人": "阻碍",
    "贵人": "大佬",
    "高人": "大佬",
    "高层": "大佬",
    "法器": "器物",
    "施法": "运用",
    "轮回": "循环",
    "报应": "后果",
    "天道": "规律",
    "命运": "人生",
    "转运": "改善",
    "化解": "解决",
    "保佑": "守护",
    "显灵": "显现",
    "灵验": "有效",
    "财运": "财富",
    "官运": "事业",
    "煞气": "负面",
    "霉运": "困境",
    "晦气": "不顺",
    "天机": "规律",
    "玄学": "学问",
    "诅咒": "诋毁",
    "中邪": "失常",
    "护身符": "吉祥物",
    "驱邪": "驱散",
    "辟邪": "防护",
    "镇宅": "守护",
    "符咒": "手段"
}

def process_folder(folder_path):
    """处理文件夹中的所有txt文件"""

    print(f"开始处理目录: {folder_path}")
    print("=" * 70)

    # 查找所有txt文件
    txt_files = glob.glob(os.path.join(folder_path, "**/*.txt"), recursive=True)
    print(f"\n找到 {len(txt_files)} 个txt文件\n")

    # 统计
    warning_removed = 0
    title_renamed = 0
    content_modified = 0
    total_title_replacements = 0
    total_content_replacements = 0

    # 第一步：删除标题中的"警告"二字
    print("【步骤1】删除标题中的'警告'二字")
    print("-" * 70)
    for file_path in txt_files[:]:  # 使用副本遍历
        file_name = os.path.basename(file_path)
        if "警告" in file_name:
            # 删除"警告"及其后面的标点符号
            new_name = re.sub(r'警告[！!：:]*', '', file_name)
            new_path = os.path.join(os.path.dirname(file_path), new_name)

            if new_name != file_name:
                os.rename(file_path, new_path)
                warning_removed += 1
                print(f"  {file_name} → {new_name}")

                # 更新文件列表
                idx = txt_files.index(file_path)
                txt_files[idx] = new_path

    if warning_removed == 0:
        print("  未发现包含'警告'的标题")
    print()

    # 第二步：替换标题敏感词
    print("【步骤2】替换标题敏感词")
    print("-" * 70)
    for file_path in txt_files[:]:  # 使用副本遍历
        file_name = os.path.basename(file_path)
        new_name = file_name
        replaced_words = []

        for sensitive, replacement in TITLE_SENSITIVE_WORDS.items():
            if sensitive in new_name:
                count = new_name.count(sensitive)
                new_name = new_name.replace(sensitive, replacement)
                replaced_words.append(f"{sensitive}→{replacement}({count}次)")
                total_title_replacements += count

        if new_name != file_name:
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
            title_renamed += 1
            print(f"  {file_name}")
            print(f"  → {new_name}")
            print(f"  替换: {', '.join(replaced_words)}\n")

            # 更新文件列表
            idx = txt_files.index(file_path)
            txt_files[idx] = new_path

    if title_renamed == 0:
        print("  未发现标题敏感词")
    print()

    # 第三步：替换内容敏感词
    print("【步骤3】替换内容敏感词")
    print("-" * 70)
    for file_path in txt_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            file_replacements = 0
            replaced_words = []

            # 替换敏感词
            for sensitive, replacement in CONTENT_SENSITIVE_WORDS.items():
                if sensitive in content:
                    count = content.count(sensitive)
                    content = content.replace(sensitive, replacement)
                    file_replacements += count
                    replaced_words.append(f"{sensitive}→{replacement}({count}次)")

            # 如果有修改，保存文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                content_modified += 1
                total_content_replacements += file_replacements

                file_name = os.path.basename(file_path)
                print(f"  {file_name}")
                print(f"  替换: {', '.join(replaced_words)}\n")

        except Exception as e:
            print(f"  [错误] {os.path.basename(file_path)}: {e}\n")

    if content_modified == 0:
        print("  未发现内容敏感词")
    print()

    # 输出统计结果
    print("=" * 70)
    print("处理完成！")
    print(f"  检查文件: {len(txt_files)} 个")
    print(f"  删除'警告': {warning_removed} 个文件")
    print(f"  重命名标题: {title_renamed} 个文件 (替换 {total_title_replacements} 次)")
    print(f"  修改内容: {content_modified} 个文件 (替换 {total_content_replacements} 次)")
    print("=" * 70)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\引导文案"

    process_folder(folder_path)
