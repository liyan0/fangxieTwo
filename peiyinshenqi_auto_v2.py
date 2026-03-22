# -*- coding: utf-8 -*-
"""
配音神器自动化脚本 - 图像匹配版
"""

import pyautogui
import pyperclip
import time
import os
import re
import random
from pathlib import Path

# 配置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 按钮图片目录
IMG_DIR = Path(r"D:\peiyinshenqi_images")

# 下载保存路径
DOWNLOAD_PATH = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频配音\流量语音"

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def find_and_click(button_name, confidence=0.7, wait=0.5, retry=3):
    """查找按钮图片并点击"""
    img_path = IMG_DIR / f"{button_name}.png"
    if not img_path.exists():
        print(f"按钮图片不存在: {img_path}")
        return False

    for i in range(retry):
        try:
            location = pyautogui.locateCenterOnScreen(str(img_path), confidence=confidence)
            if location:
                pyautogui.click(location.x, location.y)
                time.sleep(wait)
                print(f"已点击: {button_name}")
                return True
        except Exception as e:
            print(f"查找 {button_name} 出错: {e}")

        if i < retry - 1:
            print(f"未找到 {button_name}，重试 {i+2}/{retry}...")
            time.sleep(0.5)

    print(f"未找到按钮: {button_name}")
    return False

def clear_text():
    """清空文本框"""
    print("清空文本框...")
    return find_and_click("btn_clear")

def paste_text(text):
    """粘贴文本"""
    print("粘贴文本...")
    pyperclip.copy(text)
    time.sleep(0.2)
    return find_and_click("btn_paste")

def click_synthesis():
    """点击合成配音"""
    print("点击合成配音...")
    return find_and_click("btn_synthesis", confidence=0.6)

def wait_synthesis(seconds=50):
    """等待合成完成"""
    print(f"等待合成完成，约{seconds}秒...")
    for i in range(seconds, 0, -5):
        print(f"  剩余 {i} 秒...")
        time.sleep(5)

def safe_filename(name):
    """清理文件名"""
    illegal_chars = r'[\\/:*?"<>|]'
    safe = re.sub(illegal_chars, '', name)
    return safe[:80].strip() if len(safe) > 80 else safe.strip()

def handle_save_dialog(full_path):
    """处理保存对话框"""
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyperclip.copy(full_path)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)
    print(f"已保存: {full_path}")

def download_audio(filename):
    """下载配音"""
    print("下载配音...")
    ensure_dir(DOWNLOAD_PATH)
    if not find_and_click("btn_download_audio"):
        return False
    full_path = os.path.join(DOWNLOAD_PATH, f"{filename}.mp3")
    handle_save_dialog(full_path)
    return True

def download_subtitle(filename):
    """下载字幕"""
    print("下载字幕...")
    if not find_and_click("btn_download_subtitle"):
        return False
    full_path = os.path.join(DOWNLOAD_PATH, f"{filename}.srt")
    handle_save_dialog(full_path)
    return True

def test_buttons():
    """测试按钮识别"""
    print("="*50)
    print("按钮识别测试")
    print("="*50)
    print("\n请确保配音神器页面已打开并可见")
    print("5秒后开始测试...\n")
    time.sleep(5)

    buttons = ["btn_clear", "btn_paste", "btn_synthesis", "btn_download_audio", "btn_download_subtitle"]

    for btn in buttons:
        img_path = IMG_DIR / f"{btn}.png"
        if not img_path.exists():
            print(f"[X] {btn}: 图片不存在")
            continue

        try:
            location = pyautogui.locateCenterOnScreen(str(img_path), confidence=0.7)
            if location:
                print(f"[OK] {btn}: 找到位置 ({location.x}, {location.y})")
            else:
                print(f"[X] {btn}: 未找到")
        except Exception as e:
            print(f"[X] {btn}: 错误 - {e}")

    print("\n测试完成")

def test_click():
    """测试点击各按钮"""
    print("="*50)
    print("按钮点击测试")
    print("="*50)
    print("\n请确保配音神器页面已打开")
    print("5秒后依次点击各按钮...\n")
    time.sleep(5)

    print("\n1. 点击清空...")
    find_and_click("btn_clear", wait=2)

    print("\n2. 点击粘贴...")
    find_and_click("btn_paste", wait=2)

    print("\n3. 点击合成配音...")
    find_and_click("btn_synthesis", wait=2)

    print("\n4. 点击下载配音...")
    find_and_click("btn_download_audio", wait=2)

    print("\n5. 点击下载字幕...")
    find_and_click("btn_download_subtitle", wait=2)

    print("\n点击测试完成")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "find":
            test_buttons()
        elif sys.argv[1] == "click":
            test_click()
    else:
        print("用法:")
        print("  python peiyinshenqi_auto_v2.py find   - 测试按钮识别")
        print("  python peiyinshenqi_auto_v2.py click  - 测试按钮点击")
