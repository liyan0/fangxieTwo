# -*- coding: utf-8 -*-
"""
修复视频制作页面的鼠标滚轮滚动问题
"""

import os

# 读取文件
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("开始修复视频制作页面滚动问题...")

# 在视频制作页面添加鼠标滚轮绑定
old_video_scroll = '''        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")'''

new_video_scroll = '''        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")'''

if old_video_scroll in content:
    content = content.replace(old_video_scroll, new_video_scroll)
    print("  [OK] 已修复视频制作页面的鼠标滚轮绑定")
else:
    print("  [FAIL] 未找到视频制作页面的滚动代码")

# 保存修改后的文件
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("修复完成！")
print("="*50)
print("\n修复内容：")
print("1. 视频制作页面现在可以用鼠标滚轮滚动了")
print("2. 不会影响下拉框的滚动")
print("\n请重启程序测试。")
