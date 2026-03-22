# -*- coding: utf-8 -*-
"""批量替换文案中的敏感词"""
import os
import glob

# 敏感词替换映射
SENSITIVE_WORDS = {
    "点赞": "支持",
    "评论": "交流",
    "留言": "互动",
    "好运": "吉祥",
    "翻身": "转变",
    "福报": "回报",
    "福气": "祥瑞",
    "小人": "阻碍",
    "贵人": "大佬",
    "高人": "大佬",
    "高层": "大佬",
    "天选": "认可",
    "法器": "器物",
    "施法": "运用",
    "轮回": "循环",
    "报应": "后果",
    "天道": "规律",
    "因果": "关联",
    "命运": "人生",
    "转运": "改善",
    "化解": "解决",
    "破解": "应对",
    "保佑": "守护",
    "显灵": "显现",
    "灵验": "有效",
    "财运": "财富",
    "桃花运": "感情",
    "官运": "事业",
    "煞气": "负面",
    "霉运": "困境",
    "晦气": "不顺",
    "天意": "自然",
    "天机": "规律",
    "玄学": "学问"
}

# 目标文件夹
folder_path = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案"

# 查找所有txt文件
txt_files = glob.glob(os.path.join(folder_path, "**/*.txt"), recursive=True)

print(f"找到 {len(txt_files)} 个txt文件")
print("=" * 60)

modified_count = 0
total_replacements = 0

for file_path in txt_files:
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        file_replacements = 0
        replaced_words = []

        # 替换敏感词
        for sensitive, replacement in SENSITIVE_WORDS.items():
            if sensitive in content:
                count = content.count(sensitive)
                content = content.replace(sensitive, replacement)
                file_replacements += count
                replaced_words.append(f"{sensitive}->{replacement}({count}次)")

        # 如果有修改，保存文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            modified_count += 1
            total_replacements += file_replacements

            file_name = os.path.basename(file_path)
            print(f"\n[修改] {file_name}")
            print(f"  替换: {', '.join(replaced_words)}")

    except Exception as e:
        print(f"\n[错误] {os.path.basename(file_path)}: {e}")

print("\n" + "=" * 60)
print(f"处理完成！")
print(f"  检查文件: {len(txt_files)} 个")
print(f"  修改文件: {modified_count} 个")
print(f"  总替换次数: {total_replacements} 次")
