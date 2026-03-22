# -*- coding: utf-8 -*-
"""
配音神器自动化测试
1. 打开比特浏览器#11
2. 点击清空，如果有弹窗点击"立即清除"
3. 点击编辑区域，输入文案
4. 点击云泽-通用音色
5. 选择语速1.2倍慢速
6. 选择情感强度2倍
7. 点击合成配音
"""

import requests
import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 下载目录
DOWNLOAD_DIR = r"C:\Users\Administrator\Downloads\11"
# 最终保存目录
SAVE_DIR = r"D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频配音\流量语音"

def get_all_files(directory):
    """获取目录中所有文件（排除临时文件）"""
    files = set()
    for f in os.listdir(directory):
        full_path = os.path.join(directory, f)
        if os.path.isfile(full_path) and not f.endswith('.crdownload') and not f.endswith('.tmp'):
            files.add(full_path)
    return files

def wait_for_new_file(directory, before_files, timeout=30):
    """等待新文件下载完成"""
    for _ in range(timeout):
        current_files = get_all_files(directory)
        new_files = current_files - before_files
        if new_files:
            new_file = list(new_files)[0]
            time.sleep(0.5)  # 等待文件写入完成
            return new_file
        time.sleep(1)
    return None

def rename_file(old_path, new_name):
    """重命名文件，保留扩展名"""
    if not old_path or not os.path.exists(old_path):
        return None
    directory = os.path.dirname(old_path)
    extension = os.path.splitext(old_path)[1]
    new_path = os.path.join(directory, new_name + extension)
    # 如果目标文件已存在，先删除
    if os.path.exists(new_path):
        os.remove(new_path)
    os.rename(old_path, new_path)
    return new_path

# 比特浏览器API
BITBROWSER_API = "http://127.0.0.1:54345"
BROWSER_ID = "fd66587b053346ddb01a3892cea21ceb"  # 序号11的浏览器ID
CHROMEDRIVER_PATH = r"C:\Users\Administrator\AppData\Roaming\BitBrowser\chromedriver\140\chromedriver.exe"

STEP_DELAY = 2  # 每步间隔2秒

def open_browser():
    """打开比特浏览器#11"""
    print("正在打开比特浏览器#11...")
    url = f"{BITBROWSER_API}/browser/open"
    data = {"id": BROWSER_ID}
    resp = requests.post(url, json=data)
    result = resp.json()

    if result.get("success"):
        ws_url = result["data"]["ws"]
        print(f"浏览器已打开，WebSocket: {ws_url}")
        port = ws_url.split(":")[2].split("/")[0]
        return port
    else:
        print(f"打开失败: {result}")
        return None

def connect_browser(port):
    """连接到浏览器"""
    print(f"连接浏览器端口: {port}")
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run():
    # 1. 打开浏览器
    port = open_browser()
    if not port:
        print("无法打开浏览器")
        return

    time.sleep(STEP_DELAY)

    # 2. 连接浏览器
    driver = connect_browser(port)
    print(f"当前页面: {driver.current_url}")

    # 确保在配音神器页面
    if "peiyinshenqi" not in driver.current_url:
        print("跳转到配音神器页面...")
        driver.get("https://peiyinshenqi.com/tts/index")
        time.sleep(3)

    # ========== 步骤1: 点击清空按钮 ==========
    print("\n[步骤1] 点击清空按钮...")
    js_clear = '''
    var links = document.querySelectorAll('.el-link--inner');
    for(var i=0; i<links.length; i++){
        if(links[i].innerText.includes('清空')){
            links[i].click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_clear)
    time.sleep(1)

    # 检查弹窗，点击"立即清除"
    print("检查弹窗...")
    js_confirm = '''
    var btns = document.querySelectorAll('.el-message-box__btns button');
    for(var i=0; i<btns.length; i++){
        if(btns[i].innerText.includes('清除') || btns[i].innerText.includes('确定')){
            btns[i].click();
            return '已点击: ' + btns[i].innerText;
        }
    }
    return '无弹窗';
    '''
    result = driver.execute_script(js_confirm)
    print(f"弹窗处理: {result}")
    time.sleep(STEP_DELAY)

    # ========== 步骤2: 点击编辑区域并输入文案 ==========
    print("\n[步骤2] 点击编辑区域...")
    js_click_editor = '''
    var editor = document.querySelector('.editor[contenteditable="true"]');
    if(editor){
        editor.click();
        editor.focus();
        return true;
    }
    return false;
    '''
    driver.execute_script(js_click_editor)
    time.sleep(STEP_DELAY)

    print("输入文案...")
    text = "我是一个小笨蛋，" * 300
    filename = "我是一个小笨蛋"
    js_input = f'''
    var editor = document.querySelector('.editor[contenteditable="true"]');
    if(editor){{
        editor.innerText = "{text}";
        editor.dispatchEvent(new Event('input', {{bubbles: true}}));
        return true;
    }}
    return false;
    '''
    driver.execute_script(js_input)
    print(f"已输入: {text}")
    time.sleep(STEP_DELAY)

    # ========== 步骤3: 点击云泽-通用音色 ==========
    print("\n[步骤3] 点击云泽-通用音色...")
    js_voice = '''
    var items = document.querySelectorAll('.voice-name');
    for(var i=0; i<items.length; i++){
        if(items[i].innerText.includes('云泽-通用')){
            items[i].closest('.sub-item-txt').click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_voice)
    time.sleep(STEP_DELAY)

    # ========== 步骤4: 选择语速1.2倍慢速 ==========
    print("\n[步骤4] 点击语速下拉框...")
    js_speed_click = '''
    var inputs = document.querySelectorAll('.el-input__inner');
    for(var i=0; i<inputs.length; i++){
        if(inputs[i].placeholder && inputs[i].placeholder.includes('语速')){
            inputs[i].click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_speed_click)
    time.sleep(STEP_DELAY)

    print("选择1.2倍慢速...")
    js_speed_select = '''
    var options = document.querySelectorAll('.el-select-dropdown__item');
    for(var i=0; i<options.length; i++){
        if(options[i].innerText.includes('1.2') && options[i].innerText.includes('慢')){
            options[i].click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_speed_select)
    time.sleep(STEP_DELAY)

    # ========== 步骤5: 选择情感强度2倍 ==========
    print("\n[步骤5] 点击情感强度选择2倍...")
    js_emotion = '''
    var titles = document.querySelectorAll('.select-title');
    for(var i=0; i<titles.length; i++){
        if(titles[i].innerText.includes('情感强度')){
            var parent = titles[i].closest('.select-item') || titles[i].parentElement;
            var options = parent.querySelectorAll('span, div');
            for(var j=0; j<options.length; j++){
                if(options[j].innerText === '2倍' || options[j].innerText.includes('2倍情感')){
                    options[j].click();
                    return '已选择2倍';
                }
            }
        }
    }
    // 尝试直接查找2倍选项
    var allSpans = document.querySelectorAll('span');
    for(var k=0; k<allSpans.length; k++){
        if(allSpans[k].innerText === '2倍'){
            allSpans[k].click();
            return '已点击2倍';
        }
    }
    return false;
    '''
    result = driver.execute_script(js_emotion)
    print(f"情感强度: {result}")
    time.sleep(STEP_DELAY)

    # ========== 步骤6: 点击合成配音 ==========
    print("\n[步骤6] 点击合成配音...")
    js_synthesis = '''
    var btns = document.querySelectorAll('.el-button--primary');
    for(var i=0; i<btns.length; i++){
        if(btns[i].innerText.includes('合成配音')){
            btns[i].click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_synthesis)
    print("已点击合成配音")
    time.sleep(STEP_DELAY)

    # ========== 步骤7: 检查弹窗，点击"开始合成" ==========
    print("\n[步骤7] 检查是否有弹窗...")
    js_confirm_synthesis = '''
    var btns = document.querySelectorAll('.el-button--primary');
    for(var i=0; i<btns.length; i++){
        if(btns[i].innerText.includes('开始合成')){
            btns[i].click();
            return '已点击开始合成';
        }
    }
    return '无弹窗';
    '''
    result = driver.execute_script(js_confirm_synthesis)
    print(f"弹窗处理: {result}")
    time.sleep(STEP_DELAY)

    # ========== 步骤8: 等待合成完成（loading消失） ==========
    print("\n[步骤8] 等待合成完成...")
    max_wait = 120  # 最多等待120秒
    for i in range(max_wait):
        # 检查loading遮罩是否存在
        js_check_loading = '''
        var mask = document.querySelector('.el-loading-mask.is-fullscreen');
        if(mask){
            var style = window.getComputedStyle(mask);
            if(style.display !== 'none'){
                var text = mask.querySelector('.el-loading-text');
                return text ? text.innerText : 'loading';
            }
        }
        return null;
        '''
        loading_status = driver.execute_script(js_check_loading)

        if loading_status is None:
            print(f"合成完成! (等待了{i+1}秒)")
            break
        else:
            if i % 5 == 0:
                print(f"  {loading_status} ({i}秒)")
        time.sleep(1)
    else:
        print("等待超时，继续尝试下载...")

    time.sleep(STEP_DELAY)

    # ========== 步骤9: 点击下载配音 ==========
    print("\n[步骤9] 点击下载配音...")

    # 记录下载前的所有文件
    before_files = get_all_files(DOWNLOAD_DIR)

    js_download = '''
    var btns = document.querySelectorAll('.el-button');
    for(var i=0; i<btns.length; i++){
        if(btns[i].innerText.includes('下载配音')){
            btns[i].click();
            return true;
        }
    }
    return false;
    '''
    driver.execute_script(js_download)
    print("已点击下载配音")

    # 等待新文件下载完成并重命名
    print(f"等待配音下载完成...")
    new_file = wait_for_new_file(DOWNLOAD_DIR, before_files, timeout=30)
    if new_file:
        renamed = rename_file(new_file, filename)
        print(f"配音已保存: {renamed}")
    else:
        print("配音下载超时或失败")

    time.sleep(STEP_DELAY)

    # ========== 步骤10: 点击下载字幕 ==========
    print("\n[步骤10] 点击下载字幕...")

    # 先确保配音合成的loading已经完全消失
    time.sleep(1)

    # 记录下载前的所有文件
    before_files = get_all_files(DOWNLOAD_DIR)

    # 点击下载字幕按钮（找带preview-btn类的按钮或包含下载字幕文字的按钮）
    js_download_subtitle = '''
    // 方法1: 找带preview-btn类的按钮
    var previewBtns = document.querySelectorAll('button[classs="preview-btn"]');
    for(var i=0; i<previewBtns.length; i++){
        if(previewBtns[i].innerText.includes('下载字幕')){
            previewBtns[i].click();
            return '方法1: 已点击preview-btn';
        }
    }
    // 方法2: 找el-icon-chat-dot-square图标旁边的按钮
    var icons = document.querySelectorAll('.el-icon-chat-dot-square');
    for(var i=0; i<icons.length; i++){
        var btn = icons[i].closest('button');
        if(btn){
            btn.click();
            return '方法2: 已点击图标按钮';
        }
    }
    // 方法3: 遍历所有按钮找下载字幕
    var btns = document.querySelectorAll('button');
    for(var i=0; i<btns.length; i++){
        if(btns[i].innerText.includes('下载字幕') && !btns[i].querySelector('button')){
            btns[i].click();
            return '方法3: 已点击按钮 ' + btns[i].className;
        }
    }
    return '未找到下载字幕按钮';
    '''
    result = driver.execute_script(js_download_subtitle)
    print(f"下载字幕: {result}")

    # 等待字幕解析loading消失
    print("等待字幕解析...")
    time.sleep(1)  # 先等1秒让loading出现
    max_wait_subtitle = 60
    for i in range(max_wait_subtitle):
        js_check_loading = '''
        var mask = document.querySelector('.el-loading-mask.is-fullscreen');
        if(mask){
            var style = window.getComputedStyle(mask);
            if(style.display !== 'none'){
                var text = mask.querySelector('.el-loading-text');
                return text ? text.innerText : 'loading';
            }
        }
        return null;
        '''
        loading_status = driver.execute_script(js_check_loading)

        if loading_status is None:
            print(f"字幕解析完成! (等待了{i+1}秒)")
            break
        else:
            if i % 5 == 0:
                print(f"  {loading_status} ({i}秒)")
        time.sleep(1)
    else:
        print("等待超时，继续...")

    # 等待新文件下载完成并重命名
    print(f"等待字幕下载完成...")
    new_file = wait_for_new_file(DOWNLOAD_DIR, before_files, timeout=30)
    srt_file = None
    if new_file:
        renamed = rename_file(new_file, filename)
        srt_file = renamed
        print(f"字幕已保存: {renamed}")
    else:
        print("字幕下载超时或失败")

    # ========== 步骤11: 转移文件到最终目录 ==========
    print("\n[步骤11] 转移文件到最终目录...")
    import shutil

    # 确保目标目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # 转移配音文件
    mp3_src = os.path.join(DOWNLOAD_DIR, filename + ".mp3")
    if os.path.exists(mp3_src):
        mp3_dst = os.path.join(SAVE_DIR, filename + ".mp3")
        if os.path.exists(mp3_dst):
            os.remove(mp3_dst)
        shutil.move(mp3_src, mp3_dst)
        print(f"配音已转移: {mp3_dst}")

    # 转移字幕文件
    if srt_file and os.path.exists(srt_file):
        ext = os.path.splitext(srt_file)[1]
        srt_dst = os.path.join(SAVE_DIR, filename + ext)
        if os.path.exists(srt_dst):
            os.remove(srt_dst)
        shutil.move(srt_file, srt_dst)
        print(f"字幕已转移: {srt_dst}")

    print("\n所有步骤执行完成!")

if __name__ == "__main__":
    run()
