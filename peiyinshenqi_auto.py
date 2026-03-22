# -*- coding: utf-8 -*-
"""
配音神器自动化脚本 - 固定坐标版
适配屏幕分辨率: 1920x1080 (根据截图判断)
"""

import pyautogui
import pyperclip
import time
import os
import re
import random

# 配置
pyautogui.FAILSAFE = True  # 鼠标移到左上角可以中断
pyautogui.PAUSE = 0.3

# 下载保存路径
DOWNLOAD_PATH = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频配音\流量语音"

# 按钮坐标（4K屏幕 3840x2160）
# 根据截图估算
COORDS = {
    'text_area': (700, 800),           # 文本输入区域中心
    'btn_paste': (60, 1394),           # 粘贴按钮
    'btn_clear': (214, 1394),          # 清空按钮
    'btn_synthesis': (1456, 1466),     # 合成配音按钮
    'btn_download_audio': (1590, 1466),   # 下载配音按钮
    'btn_download_subtitle': (1880, 1466),  # 下载字幕按钮
}

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"已创建目录: {path}")

def click_pos(name, wait=0.5):
    """点击指定位置"""
    if name in COORDS:
        x, y = COORDS[name]
        pyautogui.click(x, y)
        time.sleep(wait)
        print(f"已点击: {name} ({x}, {y})")
        return True
    print(f"未知位置: {name}")
    return False

def clear_text():
    """清空文本框"""
    print("清空文本框...")
    click_pos('btn_clear', 0.5)

def paste_text(text):
    """粘贴文本到文本框"""
    print("粘贴文本...")
    # 先复制到剪贴板
    pyperclip.copy(text)
    time.sleep(0.2)

    # 点击粘贴按钮
    click_pos('btn_paste', 0.5)

def click_synthesis():
    """点击合成配音"""
    print("点击合成配音...")
    click_pos('btn_synthesis', 1)

def wait_synthesis(seconds=50):
    """等待合成完成"""
    print(f"等待合成完成，约{seconds}秒...")
    for i in range(seconds, 0, -5):
        print(f"  剩余 {i} 秒...")
        time.sleep(5)
    print("等待完成")

def safe_filename(name):
    """清理文件名中的非法字符"""
    # 移除Windows文件名非法字符
    illegal_chars = r'[\\/:*?"<>|]'
    safe = re.sub(illegal_chars, '', name)
    # 限制长度
    if len(safe) > 80:
        safe = safe[:80]
    return safe.strip()

def handle_save_dialog(full_path):
    """处理保存对话框"""
    time.sleep(1.5)  # 等待对话框出现

    # 清空文件名输入框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)

    # 粘贴完整路径
    pyperclip.copy(full_path)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 按回车保存
    pyautogui.press('enter')
    time.sleep(2)

    print(f"已保存: {full_path}")

def download_audio(filename):
    """下载配音MP3"""
    print("下载配音...")
    ensure_dir(DOWNLOAD_PATH)

    click_pos('btn_download_audio', 1)

    full_path = os.path.join(DOWNLOAD_PATH, f"{filename}.mp3")
    handle_save_dialog(full_path)
    return True

def download_subtitle(filename):
    """下载字幕SRT"""
    print("下载字幕...")

    click_pos('btn_download_subtitle', 1)

    full_path = os.path.join(DOWNLOAD_PATH, f"{filename}.srt")
    handle_save_dialog(full_path)
    return True

def extract_title_from_article(article_text):
    """从文案中提取标题（取【标题】后的第一个标题）"""
    lines = article_text.strip().split('\n')

    in_title_section = False
    titles = []

    for line in lines:
        line = line.strip()
        if '【标题】' in line:
            in_title_section = True
            continue
        if in_title_section and line and not line.startswith('---'):
            # 这是一个标题
            titles.append(line)
            if len(titles) >= 5:
                break
        if in_title_section and line.startswith('---'):
            break

    if titles:
        # 随机选一个标题
        title = random.choice(titles)
        return safe_filename(title)

    # 如果没找到标题，用前20个字
    text = re.sub(r'[【】\n]', '', article_text)
    return safe_filename(text[:20])

def process_article(article_text, custom_title=None):
    """处理单篇文案：清空→粘贴→合成→下载"""

    # 提取或使用自定义标题
    if custom_title:
        title = safe_filename(custom_title)
    else:
        title = extract_title_from_article(article_text)

    print(f"\n{'='*50}")
    print(f"处理文案，标题: {title}")
    print("="*50)

    # 提取正文（去掉标题部分）
    body = extract_body_from_article(article_text)

    # 1. 清空
    clear_text()

    # 2. 粘贴
    paste_text(body)

    # 3. 合成（音色、语速、情感已经在页面上设置好了）
    click_synthesis()

    # 4. 等待
    wait_synthesis(50)

    # 5. 下载配音
    download_audio(title)

    # 6. 下载字幕
    download_subtitle(title)

    print(f"\n文案处理完成: {title}")
    return True

def extract_body_from_article(article_text):
    """从文案中提取正文（去掉标题部分）"""
    lines = article_text.strip().split('\n')

    body_lines = []
    skip_title = True

    for line in lines:
        # 跳过标题区域
        if '【标题】' in line:
            skip_title = True
            continue
        if skip_title and line.strip().startswith('---'):
            skip_title = False
            continue
        if not skip_title:
            body_lines.append(line)

    # 如果没有找到分隔符，返回原文
    if not body_lines:
        return article_text

    return '\n'.join(body_lines).strip()

def test_coordinates():
    """测试坐标是否正确"""
    print("="*50)
    print("坐标测试模式")
    print("="*50)
    print("\n请确保配音神器页面已打开并可见")
    print("将依次点击各个按钮位置，请观察是否正确")
    print("\n5秒后开始...")
    time.sleep(5)

    print("\n1. 点击文本区域...")
    click_pos('text_area', 2)

    print("\n2. 点击清空按钮...")
    click_pos('btn_clear', 2)

    print("\n3. 点击粘贴按钮...")
    click_pos('btn_paste', 2)

    print("\n4. 点击合成配音按钮...")
    click_pos('btn_synthesis', 2)

    print("\n5. 点击下载配音按钮...")
    click_pos('btn_download_audio', 2)

    print("\n6. 点击下载字幕按钮...")
    click_pos('btn_download_subtitle', 2)

    print("\n测试完成！请检查点击位置是否正确")

def test_single():
    """测试单篇文案处理"""
    print("="*50)
    print("单篇文案测试")
    print("="*50)
    print("\n请确保配音神器页面已打开")
    print("5秒后开始测试...")
    time.sleep(5)

    test_text = """【标题】
你的善良终会被这世界温柔以待
懂你的人都知道你有多不容易
那些深夜里你一个人扛过了多少
别怕你值得被好好对待
时间会证明你的选择是对的

---

这是一段测试文本，用于测试配音神器的自动化功能。你好，这是测试内容。"""

    process_article(test_text)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_coordinates()
        elif sys.argv[1] == "single":
            test_single()
    else:
        print("用法:")
        print("  python peiyinshenqi_auto.py test    - 测试坐标")
        print("  python peiyinshenqi_auto.py single  - 测试单篇处理")
