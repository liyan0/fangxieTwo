# -*- coding: utf-8 -*-
"""
监控配音神器的loading状态
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import time

# 连接浏览器
BITBROWSER_API = "http://127.0.0.1:54345"
BROWSER_ID = "fd66587b053346ddb01a3892cea21ceb"

url = f"{BITBROWSER_API}/browser/open"
data = {"id": BROWSER_ID}
resp = requests.post(url, json=data)
result = resp.json()
ws_url = result["data"]["ws"]
port = ws_url.split(":")[2].split("/")[0]

driver_path = r"C:\Users\Administrator\AppData\Roaming\BitBrowser\chromedriver\140\chromedriver.exe"
options = Options()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

print("已连接浏览器，准备触发合成并监控loading...")

# 先清空并输入文案
driver.execute_script('''
var links = document.querySelectorAll(".el-link--inner");
for(var i=0; i<links.length; i++){
    if(links[i].innerText.includes("清空")){
        links[i].click();
        break;
    }
}
''')
time.sleep(1)

# 点击弹窗确认
driver.execute_script('''
var btns = document.querySelectorAll(".el-message-box__btns button");
for(var i=0; i<btns.length; i++){
    if(btns[i].innerText.includes("清除")){
        btns[i].click();
        break;
    }
}
''')
time.sleep(2)

# 输入文案
driver.execute_script('''
var editor = document.querySelector(".editor[contenteditable='true']");
if(editor){
    editor.click();
    editor.focus();
}
''')
time.sleep(2)

driver.execute_script('''
var editor = document.querySelector(".editor[contenteditable='true']");
if(editor){
    editor.innerText = "测试文案，用于观察loading状态。这是一段比较长的文字，需要一定时间来合成配音。";
    editor.dispatchEvent(new Event("input", {bubbles: true}));
}
''')
time.sleep(2)

# 点击合成配音
print("点击合成配音...")
driver.execute_script('''
var btns = document.querySelectorAll(".el-button--primary");
for(var i=0; i<btns.length; i++){
    if(btns[i].innerText.includes("合成配音")){
        btns[i].click();
        break;
    }
}
''')
time.sleep(2)

# 点击开始合成
print("点击开始合成...")
driver.execute_script('''
var btns = document.querySelectorAll(".el-button--primary");
for(var i=0; i<btns.length; i++){
    if(btns[i].innerText.includes("开始合成")){
        btns[i].click();
        break;
    }
}
''')

# 立即开始监控页面元素
print("\n开始监控页面元素变化...")
for i in range(30):
    time.sleep(1)

    # 获取页面HTML片段，查找loading相关
    js_check = """
    var result = {loading: [], buttons: [], html: ''};

    // 查找所有元素
    var all = document.querySelectorAll("*");
    for(var j=0; j<all.length; j++){
        var el = all[j];
        var cls = el.className || '';
        if(typeof cls === 'string'){
            if(cls.indexOf('loading') >= 0 || cls.indexOf('mask') >= 0 || cls.indexOf('spinner') >= 0 || cls.indexOf('progress') >= 0){
                var style = window.getComputedStyle(el);
                if(style.display !== 'none' && style.visibility !== 'hidden'){
                    result.loading.push({
                        tag: el.tagName,
                        cls: cls.substring(0, 100),
                        text: (el.innerText || '').substring(0, 30)
                    });
                }
            }
        }
    }

    // 检查下载按钮状态
    var btns = document.querySelectorAll('.el-button');
    for(var k=0; k<btns.length; k++){
        var btn = btns[k];
        if(btn.innerText.indexOf('下载配音') >= 0){
            result.buttons.push({
                text: btn.innerText,
                disabled: btn.disabled,
                cls: btn.className
            });
        }
    }

    return result;
    """

    try:
        status = driver.execute_script(js_check)
        print(f"[{i+1}秒] loading元素: {len(status['loading'])}, 下载按钮: {status['buttons']}")

        if status['loading']:
            for el in status['loading'][:3]:
                print(f"    -> {el}")
    except Exception as e:
        print(f"[{i+1}秒] 错误: {e}")
