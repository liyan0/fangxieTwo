# -*- coding: utf-8 -*-
"""
手动获取按钮坐标工具
"""
import pyautogui
import json
import time

print("="*50)
print("按钮坐标获取工具")
print("="*50)
print("\n请按提示操作，把鼠标移到对应按钮上，然后按回车键记录位置\n")

coords = {}

buttons = [
    ("text_area", "文本输入框（左边大框里面）"),
    ("btn_clear", "清空按钮"),
    ("btn_paste", "粘贴按钮"),
    ("btn_synthesis", "合成配音按钮（蓝色）"),
    ("btn_download_audio", "下载配音按钮"),
    ("btn_download_subtitle", "下载字幕按钮"),
]

for key, name in buttons:
    input(f"\n请把鼠标移到【{name}】上，然后按回车...")
    x, y = pyautogui.position()
    coords[key] = (x, y)
    print(f"  已记录: {key} = ({x}, {y})")

print("\n" + "="*50)
print("所有坐标已记录：")
print("="*50)
for k, v in coords.items():
    print(f"  '{k}': {v},")

# 保存到文件
with open("D:/peiyinshenqi_images/coords.json", "w") as f:
    json.dump(coords, f, indent=2)
print(f"\n坐标已保存到: D:/peiyinshenqi_images/coords.json")
