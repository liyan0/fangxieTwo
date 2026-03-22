# -*- coding: utf-8 -*-
"""
百家号引流视频 批量生成主程序
功能：生成文案 → 批量生成视频
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 仿写文案生成器 import generate_wenan1, generate_wenan2, save_document
from video_generator_v3 import generate_video, OUTPUT_DIR, BGM_PATH


def extract_articles_from_doc(doc):
    """从文档中提取文章内容和标题"""
    articles = []
    current_title = ""
    current_content = []
    in_article = False

    for para in doc.paragraphs:
        text = para.text.strip()

        # 跳过分隔符
        if text.startswith("═") or text == "---" or not text:
            continue

        # 检测文章开始
        if text.startswith("【第") and "篇】" in text:
            if current_content:
                articles.append({
                    "title": current_title,
                    "content": "\n\n".join(current_content)
                })
                current_content = []
            in_article = True
            continue

        # 提取标题（取第一个标题）
        if text.startswith("【标题1】"):
            current_title = text.replace("【标题1】", "").strip()
            continue

        # 跳过其他标题行
        if text.startswith("【标题"):
            continue

        # 收集正文
        if in_article and text:
            current_content.append(text)

    # 添加最后一篇
    if current_content:
        articles.append({
            "title": current_title,
            "content": "\n\n".join(current_content)
        })

    return articles


def main():
    """主函数"""
    print("=" * 60)
    print("百家号引流视频 批量生成器")
    print("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ========== 步骤1: 生成文案 ==========
    print("\n【阶段1】生成仿写文案...")

    doc1 = generate_wenan1()
    doc2 = generate_wenan2()

    save_dir = "D:/A百家号带货视频/带货文案"
    os.makedirs(save_dir, exist_ok=True)

    file1 = save_document(doc1, f"{timestamp}_文案1_一人战胜一群人.docx", save_dir)
    file2 = save_document(doc2, f"{timestamp}_文案2_深爱你的人.docx", save_dir)

    print(f"  文案1已保存: {file1}")
    print(f"  文案2已保存: {file2}")

    # ========== 步骤2: 提取文章 ==========
    print("\n【阶段2】提取文章内容...")

    articles1 = extract_articles_from_doc(doc1)
    articles2 = extract_articles_from_doc(doc2)

    all_articles = []
    for i, art in enumerate(articles1):
        all_articles.append({
            "name": f"文案1_第{i+1}篇",
            "title": art["title"],
            "content": art["content"]
        })
    for i, art in enumerate(articles2):
        all_articles.append({
            "name": f"文案2_第{i+1}篇",
            "title": art["title"],
            "content": art["content"]
        })

    print(f"  共提取 {len(all_articles)} 篇文章")
    for art in all_articles:
        print(f"    - {art['name']}: {art['title'][:20]}...")

    # ========== 步骤3: 批量生成视频 ==========
    print("\n【阶段3】批量生成视频...")

    success_count = 0
    fail_count = 0

    for i, art in enumerate(all_articles):
        video_name = f"{timestamp}_{art['name']}"
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(all_articles)}] {art['title']}")
        print(f"{'='*60}")

        try:
            result = generate_video(
                text=art["content"],
                title=art["title"],
                video_name=video_name,
                bgm_path=BGM_PATH
            )
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  生成失败: {e}")
            fail_count += 1

    # ========== 完成 ==========
    print("\n" + "=" * 60)
    print("批量生成完成!")
    print("=" * 60)
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    print(f"文案保存: {save_dir}")
    print(f"视频保存: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
