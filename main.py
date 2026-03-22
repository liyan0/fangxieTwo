# -*- coding: utf-8 -*-
"""
百家号引流文案+视频 一键生成器
功能：读取参考文案 → 生成仿写文案 → 生成图片 → 合成视频
"""

import os
import sys
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 仿写文案生成器 import generate_wenan1, generate_wenan2, save_document
from video_generator import generate_video_from_text, ensure_dirs
from config import OUTPUT_DIR


def extract_content_from_doc(doc):
    """从文档中提取纯文本内容"""
    texts = []
    current_article = []
    in_article = False

    for para in doc.paragraphs:
        text = para.text.strip()

        # 跳过标题行和分隔符
        if text.startswith("【标题") or text.startswith("═") or text == "---":
            continue

        # 检测文章开始
        if text.startswith("【第") and "篇】" in text:
            if current_article:
                texts.append("\n\n".join(current_article))
                current_article = []
            in_article = True
            continue

        # 收集正文内容
        if in_article and text:
            current_article.append(text)

    # 添加最后一篇
    if current_article:
        texts.append("\n\n".join(current_article))

    return texts


def main():
    """主函数"""
    print("="*60)
    print("百家号引流文案+视频 一键生成器")
    print("="*60)

    today = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ensure_dirs()

    # 步骤1: 生成文案
    print("\n【步骤1】生成仿写文案...")

    doc1 = generate_wenan1()
    doc2 = generate_wenan2()

    save_dir = "D:/A百家号带货视频/带货文案"
    os.makedirs(save_dir, exist_ok=True)

    file1 = save_document(doc1, f"{timestamp}_文案1.docx", save_dir)
    file2 = save_document(doc2, f"{timestamp}_文案2.docx", save_dir)

    print(f"  文案1已保存: {file1}")
    print(f"  文案2已保存: {file2}")

    # 步骤2: 提取文案内容
    print("\n【步骤2】提取文案内容...")

    articles1 = extract_content_from_doc(doc1)
    articles2 = extract_content_from_doc(doc2)

    all_articles = []
    for i, text in enumerate(articles1):
        all_articles.append((f"文案1_第{i+1}篇", text))
    for i, text in enumerate(articles2):
        all_articles.append((f"文案2_第{i+1}篇", text))

    print(f"  共提取 {len(all_articles)} 篇文案")

    # 步骤3: 为每篇文案生成视频
    print("\n【步骤3】生成视频...")

    for name, text in all_articles:
        video_name = f"{timestamp}_{name}"
        print(f"\n  正在处理: {video_name}")
        try:
            generate_video_from_text(text, video_name)
        except Exception as e:
            print(f"  生成失败: {e}")
            continue

    print("\n" + "="*60)
    print("全部完成!")
    print(f"文案保存位置: {save_dir}")
    print(f"视频保存位置: {OUTPUT_DIR}")
    print("="*60)


if __name__ == "__main__":
    main()
