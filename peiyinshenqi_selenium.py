# -*- coding: utf-8 -*-
"""
配音神器自动化脚本 - Selenium版
直接控制浏览器，通过网页元素操作
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import os
import re
import random

# 下载保存路径
DOWNLOAD_PATH = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频配音\流量语音"

# 配音神器网址
URL = "https://peiyinshenqi.com/tts/index"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def safe_filename(name):
    illegal_chars = r'[\\/:*?"<>|]'
    safe = re.sub(illegal_chars, '', name)
    return safe[:80].strip() if len(safe) > 80 else safe.strip()

class PeiyinAuto:
    def __init__(self):
        self.driver = None

    def start_browser(self):
        """启动Edge浏览器"""
        print("启动浏览器...")

        options = Options()
        # 设置下载路径
        prefs = {
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }
        options.add_experimental_option("prefs", prefs)

        # 使用已有的Edge浏览器
        options.add_argument("--start-maximized")

        self.driver = webdriver.Edge(options=options)
        self.driver.get(URL)
        print(f"已打开: {URL}")
        time.sleep(3)

    def connect_existing_browser(self, debugger_address="127.0.0.1:9222"):
        """连接到已打开的浏览器"""
        print(f"连接到已有浏览器: {debugger_address}")

        options = Options()
        options.add_experimental_option("debuggerAddress", debugger_address)

        self.driver = webdriver.Edge(options=options)
        print("已连接")

    def clear_text(self):
        """清空文本框"""
        print("清空文本框...")
        try:
            # 找到清空按钮并点击
            clear_btn = self.driver.find_element(By.XPATH, "//span[contains(text(),'清空')]")
            clear_btn.click()
            time.sleep(0.5)
            print("已清空")
            return True
        except Exception as e:
            print(f"清空失败: {e}")
            return False

    def paste_text(self, text):
        """输入文本"""
        print("输入文本...")
        try:
            # 找到文本输入框
            textarea = self.driver.find_element(By.TAG_NAME, "textarea")
            textarea.clear()
            textarea.send_keys(text)
            time.sleep(0.5)
            print("已输入文本")
            return True
        except Exception as e:
            print(f"输入失败: {e}")
            return False

    def select_voice(self, voice_name="云泽"):
        """选择音色"""
        print(f"选择音色: {voice_name}...")
        try:
            # 找到音色选项并点击
            voice = self.driver.find_element(By.XPATH, f"//div[contains(text(),'{voice_name}')]")
            voice.click()
            time.sleep(0.5)
            print(f"已选择: {voice_name}")
            return True
        except Exception as e:
            print(f"选择音色失败: {e}")
            return False

    def click_synthesis(self):
        """点击合成配音"""
        print("点击合成配音...")
        try:
            # 找到合成配音按钮
            btn = self.driver.find_element(By.XPATH, "//span[contains(text(),'合成配音')]")
            btn.click()
            print("已点击合成")
            return True
        except Exception as e:
            print(f"点击合成失败: {e}")
            return False

    def wait_synthesis(self, max_wait=60):
        """等待合成完成"""
        print(f"等待合成完成，最多{max_wait}秒...")

        for i in range(max_wait):
            try:
                # 检查下载按钮是否可用
                download_btn = self.driver.find_element(By.XPATH, "//span[contains(text(),'下载配音')]")
                parent = download_btn.find_element(By.XPATH, "./..")
                if "disabled" not in parent.get_attribute("class"):
                    print("合成完成!")
                    return True
            except:
                pass

            if i % 10 == 0:
                print(f"  已等待 {i} 秒...")
            time.sleep(1)

        print("等待超时")
        return False

    def download_audio(self):
        """下载配音"""
        print("下载配音...")
        try:
            btn = self.driver.find_element(By.XPATH, "//span[contains(text(),'下载配音')]")
            btn.click()
            time.sleep(2)
            print("已点击下载配音")
            return True
        except Exception as e:
            print(f"下载配音失败: {e}")
            return False

    def download_subtitle(self):
        """下载字幕"""
        print("下载字幕...")
        try:
            btn = self.driver.find_element(By.XPATH, "//span[contains(text(),'下载字幕')]")
            btn.click()
            time.sleep(2)
            print("已点击下载字幕")
            return True
        except Exception as e:
            print(f"下载字幕失败: {e}")
            return False

    def process_article(self, text, title):
        """处理单篇文案"""
        print(f"\n{'='*50}")
        print(f"处理: {title[:30]}...")
        print("="*50)

        # 1. 清空
        self.clear_text()

        # 2. 输入文本
        self.paste_text(text)

        # 3. 点击合成
        self.click_synthesis()

        # 4. 等待合成
        if not self.wait_synthesis(60):
            print("合成超时，跳过")
            return False

        # 5. 下载
        self.download_audio()
        time.sleep(1)
        self.download_subtitle()

        print(f"完成: {title}")
        return True

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def test():
    """测试"""
    print("="*50)
    print("配音神器Selenium测试")
    print("="*50)

    auto = PeiyinAuto()

    try:
        # 启动浏览器
        auto.start_browser()

        input("\n浏览器已打开，请确认页面加载完成后按回车继续...")

        # 测试清空
        print("\n测试清空...")
        auto.clear_text()

        # 测试输入
        print("\n测试输入...")
        auto.paste_text("这是一段测试文本，用于测试配音神器自动化。")

        input("\n按回车测试合成...")

        # 测试合成
        auto.click_synthesis()
        auto.wait_synthesis(30)

    except Exception as e:
        print(f"测试出错: {e}")
    finally:
        input("\n按回车关闭浏览器...")
        auto.close()

if __name__ == "__main__":
    test()
