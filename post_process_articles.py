#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文案后处理脚本 - 自动检查和清理生成的文案
功能：
1. 删除不通顺的英文片段
2. 替换敏感词为安全词语
"""

import os
import re
import sys

# 敏感词映射表
SENSITIVE_WORDS = {
    "福报": "好运",
    "大运": "好运",
    "渡劫": "历练",
    "贵人": "恩人",
    "小人": "坏人",
    "财运": "财路",
    "运气": "运势",
    "法宝": "好物",
    "法器": "物品",
    "护身符": "守护物",
    "评论区": "留言",
    "点赞": "支持",
    "收藏": "保存",
    "算命": "预测",
    "占卜": "推测",
    "卜卦": "推算",
    "看相": "观察",
    "面相": "面貌",
    "手相": "手纹",
    "八字": "命理",
    "符咒": "符号",
    "画符": "绘制",
    "念咒": "念诵",
    "做法": "仪式",
    "施法": "操作",
    "法术": "方法",
    "巫术": "技艺",
    "菩萨": "高人",
    "观音": "高人",
    "如来": "高人",
    "阎王": "判官",
    "地狱": "困境",
    "天堂": "美好",
    "转世": "重生",
    "投胎": "新生",
    "烧香拜佛": "祈福",
    "上香磕头": "祈愿",
    "跪拜供奉": "敬奉",
    "改运": "改变",
    "转运": "转变",
    "开光": "启用",
    "法事": "仪式",
}

def remove_english_fragments(text):
    """删除不通顺的英文片段（保留常见专有名词）"""
    # 保留的英文词（常见专有名词、缩写等）
    keep_words = ['AI', 'APP', 'CEO', 'VIP', 'OK', 'NO']
    
    # 匹配连续的英文字母（3个以上）
    pattern = r'\b[A-Za-z]{3,}\b'
    
    def replace_func(match):
        word = match.group(0)
        # 如果是保留词，不删除
        if word.upper() in keep_words:
            return word
        # 否则删除
        return ''
    
    # 替换英文片段
    text = re.sub(pattern, replace_func, text)
    
    # 清理多余的空格
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([，。！？、；：])', r'\1', text)
    
    return text.strip()

def replace_sensitive_words(text):
    """替换敏感词"""
    for sensitive, safe in SENSITIVE_WORDS.items():
        text = text.replace(sensitive, safe)
    return text

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 删除英文片段
        content = remove_english_fragments(content)
        
        # 2. 替换敏感词
        content = replace_sensitive_words(content)
        
        # 如果内容有变化，保存文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, filepath
        
        return False, None
        
    except Exception as e:
        print(f"处理文件失败 {filepath}: {str(e)}")
        return False, None

def process_directory(directory):
    """处理目录中的所有txt文件"""
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return
    
    modified_files = []
    total_files = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            total_files += 1
            modified, path = process_file(filepath)
            if modified:
                modified_files.append(os.path.basename(path))
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"修改文件数: {len(modified_files)}")
    
    if modified_files:
        print(f"\n已修改的文件:")
        for f in modified_files:
            print(f"  - {f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # 默认处理流量文案目录
        directory = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案"
    
    print(f"开始处理目录: {directory}")
    process_directory(directory)
