# -*- coding: utf-8 -*-
"""
自动配音模块 v2 - 使用 pyautogui 直接操作已打开的浏览器
不需要 Selenium，直接操作你已经登录好的浏览器
"""

import time
import os
import pyautogui
import pyperclip
import subprocess

# 设置 pyautogui 安全设置
pyautogui.FAILSAFE = True  # 鼠标移到左上角可以中断
pyautogui.PAUSE = 0.3  # 每个操作之间暂停0.3秒

class AutoDubbing:
    def __init__(self, download_dir="D:\\A百家号带货视频\\A带货配音"):
        self.download_dir = download_dir
        self.url = "https://peiyinshenqi.com/tts/index"

        # 确保下载目录存在
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def activate_chrome(self):
        """激活Chrome浏览器窗口"""
        import pygetwindow as gw
        try:
            # 查找Chrome窗口
            chrome_windows = gw.getWindowsWithTitle('Chrome')
            if chrome_windows:
                chrome_windows[0].activate()
                time.sleep(0.5)
                return True

            # 如果没找到，尝试其他标题
            chrome_windows = gw.getWindowsWithTitle('Google Chrome')
            if chrome_windows:
                chrome_windows[0].activate()
                time.sleep(0.5)
                return True

            print("未找到Chrome窗口")
            return False
        except Exception as e:
            print(f"激活Chrome失败: {e}")
            return False

    def open_website(self):
        """打开配音神器网站"""
        # 激活Chrome
        if not self.activate_chrome():
            print("请手动打开Chrome浏览器")
            return False

        # Ctrl+T 打开新标签页
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.5)

        # 输入网址
        pyautogui.typewrite(self.url, interval=0.02)
        pyautogui.press('enter')

        print(f"已打开: {self.url}")
        time.sleep(3)  # 等待页面加载
        return True

    def open_website_in_current_tab(self):
        """在当前标签页打开配音神器（如果已经在配音神器页面则刷新）"""
        if not self.activate_chrome():
            print("请手动打开Chrome浏览器")
            return False

        # Ctrl+L 选中地址栏
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)

        # 输入网址
        pyperclip.copy(self.url)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')

        print(f"已打开: {self.url}")
        time.sleep(3)
        return True

    def paste_text(self, text):
        """粘贴文案到文本框"""
        try:
            # 复制文案到剪贴板
            pyperclip.copy(text)

            # 4K屏幕，文本框在左侧区域
            # 大约在 X=700, Y=800 的位置（根据屏幕比例估算）
            click_x = 700
            click_y = 800

            pyautogui.click(click_x, click_y)
            time.sleep(0.3)

            # Ctrl+A 全选（清除原有内容）
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)

            # Ctrl+V 粘贴
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

            print(f"已粘贴文案，共 {len(text)} 字")
            return True
        except Exception as e:
            print(f"粘贴文案失败: {e}")
            return False

    def click_synthesize(self):
        """点击合成配音按钮"""
        try:
            # 合成按钮位置：X=1951, Y=1963
            click_x = 1951
            click_y = 1963

            pyautogui.click(click_x, click_y)
            print(f"已点击合成配音按钮 ({click_x}, {click_y})")
            time.sleep(1.5)

            # 检查是否有确认弹窗（尝试点击确认按钮位置）
            # 如果有弹窗，点击确认；如果没有，点击也不会有影响
            screen_width, screen_height = pyautogui.size()
            confirm_x = screen_width // 2
            confirm_y = screen_height // 2 + 50

            # 尝试点击确认（有弹窗就确认，没有也无妨）
            pyautogui.click(confirm_x, confirm_y)
            print(f"已尝试点击确认按钮 ({confirm_x}, {confirm_y})")
            time.sleep(0.5)

            return True
        except Exception as e:
            print(f"点击合成按钮失败: {e}")
            return False

    def wait_for_synthesis(self, text_length):
        """根据文案长度等待合成完成"""
        # 大约每100字需要10-15秒合成时间
        base_time = 20  # 基础等待时间增加到20秒
        extra_time = (text_length // 100) * 10  # 每100字额外等待10秒
        wait_time = base_time + extra_time

        # 最少等25秒，最多等300秒
        wait_time = max(25, min(wait_time, 300))

        print(f"文案长度: {text_length} 字，预计等待: {wait_time} 秒")

        # 分段等待，显示进度
        for i in range(wait_time // 5):
            time.sleep(5)
            print(f"  合成中... {(i+1)*5}/{wait_time}秒")

        # 剩余时间
        remaining = wait_time % 5
        if remaining > 0:
            time.sleep(remaining)

        print("合成应该完成了")
        return wait_time

    def wait_and_download(self, text_length=100, timeout=120):
        """等待合成完成并下载"""
        print(f"等待合成完成...")

        # 根据文案长度等待
        self.wait_for_synthesis(text_length)

        # 先激活浏览器窗口
        self.activate_chrome()
        time.sleep(0.5)

        # 下载按钮位置：X=2144, Y=1969
        click_x = 2144
        click_y = 1969

        # 点击两次确保点到
        print(f"点击下载按钮 ({click_x}, {click_y})...")
        pyautogui.click(click_x, click_y)
        time.sleep(1)
        pyautogui.click(click_x, click_y)
        print(f"已点击下载按钮")
        time.sleep(3)

        return True

    def process_article(self, text, voice_name="云泽"):
        """处理单篇文案的完整流程"""
        print("=" * 50)
        print("开始自动配音流程")
        print("=" * 50)

        # 1. 打开网站
        print("\n[1/4] 打开配音神器网站...")
        if not self.open_website_in_current_tab():
            return False

        # 2. 粘贴文案
        print("\n[2/4] 粘贴文案...")
        time.sleep(2)  # 等待页面完全加载
        if not self.paste_text(text):
            return False

        # 3. 点击合成
        print("\n[3/4] 点击合成配音...")
        time.sleep(1)
        if not self.click_synthesize():
            return False

        # 4. 等待并下载
        print("\n[4/4] 等待合成完成并下载...")
        self.wait_and_download(text_length=len(text))

        print("\n" + "=" * 50)
        print("配音流程完成！")
        print(f"文件保存位置: {self.download_dir}")
        print("=" * 50)
        return True

    def close(self):
        """关闭（这个版本不需要关闭浏览器）"""
        pass


def test():
    """测试函数"""
    # 先安装 pygetwindow
    try:
        import pygetwindow
    except ImportError:
        print("安装 pygetwindow...")
        import subprocess
        subprocess.run(["pip", "install", "pygetwindow"], check=True)

    test_text = """你好，这是一段测试文案。

今天我们来聊一聊人生的道理。

希望这段配音能够成功合成。"""

    dubbing = AutoDubbing()

    print("3秒后开始，请确保Chrome浏览器已打开...")
    time.sleep(3)

    dubbing.process_article(test_text)


if __name__ == "__main__":
    test()
