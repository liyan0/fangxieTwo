# -*- coding: utf-8 -*-
"""
自动配音模块 - 使用配音神器网站自动合成配音
"""

import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pyautogui
import pyperclip

class AutoDubbing:
    def __init__(self, download_dir="D:\\A百家号带货视频\\A带货配音"):
        self.download_dir = download_dir
        self.url = "https://peiyinshenqi.com/tts/index"
        self.driver = None
        self.chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.debug_port = 9222

        # 确保下载目录存在
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def start_chrome_debug_mode(self):
        """以调试模式启动Chrome（如果还没启动）"""
        # 检查是否已经有调试模式的Chrome在运行
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', self.debug_port))
        sock.close()

        if result != 0:
            # 没有运行，启动新的Chrome
            print("启动Chrome调试模式...")
            cmd = f'"{self.chrome_path}" --remote-debugging-port={self.debug_port}'
            subprocess.Popen(cmd, shell=True)
            time.sleep(3)
        else:
            print("Chrome调试模式已在运行")

    def connect_to_existing_browser(self):
        """连接到已经打开的Chrome浏览器"""
        self.start_chrome_debug_mode()

        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.debug_port}")

        # 设置下载目录
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        print("已连接到现有Chrome浏览器")
        return self.driver

    def start_browser(self):
        """启动浏览器 - 使用已有的Chrome用户数据保持登录状态"""
        chrome_options = Options()

        # 使用已有的Chrome用户数据目录，保持登录状态
        user_data_dir = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data"
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument("--profile-directory=Default")

        # 设置下载目录
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # 保持浏览器打开
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        print("已启动Chrome（使用已有登录状态）")
        return self.driver

    def open_website(self):
        """打开配音神器网站"""
        if not self.driver:
            self.start_browser()

        self.driver.get(self.url)
        time.sleep(3)  # 等待页面加载

    def paste_text(self, text):
        """粘贴文案到文本框"""
        try:
            # 等待页面完全加载
            time.sleep(2)

            # 方法1: 尝试直接找到 editor div
            try:
                editor = self.driver.find_element(By.CSS_SELECTOR, "div.editor[contenteditable='true']")
                editor.click()
                time.sleep(0.5)

                # 使用 JavaScript 设置内容
                html_text = text.replace('\n', '<br>')
                self.driver.execute_script("arguments[0].innerHTML = arguments[1];", editor, html_text)
                print(f"已粘贴文案（方法1），共 {len(text)} 字")
                return True
            except Exception as e1:
                print(f"方法1失败: {e1}")

            # 方法2: 使用剪贴板 + pyautogui
            try:
                import pyperclip
                pyperclip.copy(text)

                # 点击页面中间偏左的位置（文本框区域）
                pyautogui.click(400, 400)
                time.sleep(0.5)

                # Ctrl+A 全选，然后 Ctrl+V 粘贴
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)

                print(f"已粘贴文案（方法2-剪贴板），共 {len(text)} 字")
                return True
            except Exception as e2:
                print(f"方法2失败: {e2}")

            # 方法3: 使用 ActionChains
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys

                # 找到任意可编辑元素
                editable = self.driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")

                actions = ActionChains(self.driver)
                actions.click(editable)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(text)
                actions.perform()

                print(f"已粘贴文案（方法3），共 {len(text)} 字")
                return True
            except Exception as e3:
                print(f"方法3失败: {e3}")

            return False
        except Exception as e:
            print(f"粘贴文案失败: {e}")
            return False

    def select_voice(self, voice_name="云泽"):
        """选择配音音效"""
        try:
            # 点击音效选择区域，查找包含指定名称的元素
            wait = WebDriverWait(self.driver, 10)

            # 尝试找到音效选项
            voice_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{voice_name}')]")

            if voice_elements:
                voice_elements[0].click()
                print(f"已选择音效: {voice_name}")
                time.sleep(1)
                return True
            else:
                print(f"未找到音效: {voice_name}，使用默认音效")
                return True
        except Exception as e:
            print(f"选择音效失败: {e}")
            return True  # 继续执行，使用默认音效

    def click_synthesize(self):
        """点击合成配音按钮"""
        try:
            wait = WebDriverWait(self.driver, 10)

            # 尝试多种方式找到合成按钮
            selectors = [
                (By.XPATH, "//button[contains(., '合成')]"),
                (By.XPATH, "//*[contains(text(), '合成配音')]"),
                (By.CSS_SELECTOR, "button.el-button--primary"),
                (By.XPATH, "//i[contains(@class, 'el-icon-video-play')]/parent::button"),
                (By.XPATH, "//i[contains(@class, 'el-icon-video-play')]/ancestor::button"),
                (By.CSS_SELECTOR, "i.el-icon-video-play"),
            ]

            for by, selector in selectors:
                try:
                    elements = self.driver.find_elements(by, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            # 如果是图标，点击其父元素
                            if elem.tag_name == 'i':
                                parent = elem.find_element(By.XPATH, "./..")
                                parent.click()
                            else:
                                elem.click()
                            print("已点击合成配音按钮")
                            return True
                except:
                    continue

            # 如果还是找不到，尝试找所有按钮并点击包含"合成"文字的
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "合成" in btn.text:
                    btn.click()
                    print("已点击合成配音按钮（通过文字匹配）")
                    return True

            print("未找到合成按钮")
            return False

        except Exception as e:
            print(f"点击合成按钮失败: {e}")
            return False

    def wait_for_synthesis(self, timeout=120):
        """等待合成完成"""
        print("等待配音合成中...")

        # 等待合成完成，检测下载按钮出现
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 检查是否有下载按钮
                download_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), '下载')]")
                if download_btns:
                    print("合成完成！")
                    return True
            except:
                pass
            time.sleep(2)

        print("合成超时")
        return False

    def click_download(self):
        """点击下载配音按钮"""
        try:
            wait = WebDriverWait(self.driver, 10)

            # 尝试找到下载按钮
            selectors = [
                (By.XPATH, "//button[contains(text(), '下载')]"),
                (By.XPATH, "//*[contains(text(), '下载配音')]"),
                (By.XPATH, "//a[contains(text(), '下载')]"),
            ]

            for by, selector in selectors:
                try:
                    btn = self.driver.find_element(by, selector)
                    btn.click()
                    print("已点击下载按钮")
                    time.sleep(3)  # 等待下载开始
                    return True
                except:
                    continue

            print("未找到下载按钮")
            return False

        except Exception as e:
            print(f"点击下载按钮失败: {e}")
            return False

    def process_article(self, text, voice_name="云泽"):
        """处理单篇文案的完整流程"""
        print("=" * 50)
        print("开始自动配音流程")
        print("=" * 50)

        # 1. 打开网站
        print("\n[1/5] 打开配音神器网站...")
        self.open_website()

        # 2. 粘贴文案
        print("\n[2/5] 粘贴文案...")
        if not self.paste_text(text):
            return False

        # 3. 选择音效
        print("\n[3/5] 选择配音音效...")
        self.select_voice(voice_name)

        # 4. 点击合成
        print("\n[4/5] 点击合成配音...")
        if not self.click_synthesize():
            return False

        # 5. 等待合成并下载
        print("\n[5/5] 等待合成完成并下载...")
        if self.wait_for_synthesis():
            self.click_download()
            print("\n配音完成！文件已保存到:", self.download_dir)
            return True

        return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None


def test():
    """测试函数"""
    test_text = """你好，这是一段测试文案。

今天我们来聊一聊人生的道理。

希望这段配音能够成功合成。"""

    dubbing = AutoDubbing()
    try:
        dubbing.process_article(test_text)
        input("按回车键关闭浏览器...")
    finally:
        dubbing.close()


if __name__ == "__main__":
    test()
