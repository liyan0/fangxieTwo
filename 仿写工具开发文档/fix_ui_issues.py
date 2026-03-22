# -*- coding: utf-8 -*-
"""
修复UI问题：
1. 文件夹选择对话框初始目录问题
2. 下拉框滚动时主页面也滚动的问题
"""

import os

# 读取文件
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("开始修复UI问题...")

# ========== 修复1：文件夹选择初始目录 ==========
print("\n[修复1] 添加文件夹选择初始目录...")

# 修复 select_txt_output_folder
old_txt_output = '''    def select_txt_output_folder(self):
        """选择TXT保存文件夹"""
        folder_path = filedialog.askdirectory(title="选择TXT保存文件夹")
        if folder_path:
            self.txt_output_path.set(folder_path)'''

new_txt_output = '''    def select_txt_output_folder(self):
        """选择TXT保存文件夹"""
        current_path = self.txt_output_path.get()
        initial_dir = current_path if current_path and os.path.exists(current_path) else None
        folder_path = filedialog.askdirectory(title="选择TXT保存文件夹", initialdir=initial_dir)
        if folder_path:
            self.txt_output_path.set(folder_path)'''

if old_txt_output in content:
    content = content.replace(old_txt_output, new_txt_output)
    print("  [OK] 已修复 select_txt_output_folder")
else:
    print("  [FAIL] 未找到 select_txt_output_folder")

# 修复 select_voice_input_folder
old_voice_input = '''    def select_voice_input_folder(self):
        """选择语音合成的文案输入目录"""
        folder_path = filedialog.askdirectory(title="选择文案目录")
        if folder_path:
            self.voice_input_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_input_path"] = folder_path
            save_config(self.config)'''

new_voice_input = '''    def select_voice_input_folder(self):
        """选择语音合成的文案输入目录"""
        current_path = self.voice_input_path.get()
        initial_dir = current_path if current_path and os.path.exists(current_path) else None
        folder_path = filedialog.askdirectory(title="选择文案目录", initialdir=initial_dir)
        if folder_path:
            self.voice_input_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_input_path"] = folder_path
            save_config(self.config)'''

if old_voice_input in content:
    content = content.replace(old_voice_input, new_voice_input)
    print("  [OK] 已修复 select_voice_input_folder")
else:
    print("  [FAIL] 未找到 select_voice_input_folder")

# 修复 select_voice_output_folder
old_voice_output = '''    def select_voice_output_folder(self):
        """选择语音合成的输出目录"""
        folder_path = filedialog.askdirectory(title="选择配音输出目录")
        if folder_path:
            self.voice_output_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_output_path"] = folder_path
            save_config(self.config)'''

new_voice_output = '''    def select_voice_output_folder(self):
        """选择语音合成的输出目录"""
        current_path = self.voice_output_path.get()
        initial_dir = current_path if current_path and os.path.exists(current_path) else None
        folder_path = filedialog.askdirectory(title="选择配音输出目录", initialdir=initial_dir)
        if folder_path:
            self.voice_output_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_output_path"] = folder_path
            save_config(self.config)'''

if old_voice_output in content:
    content = content.replace(old_voice_output, new_voice_output)
    print("  [OK] 已修复 select_voice_output_folder")
else:
    print("  [FAIL] 未找到 select_voice_output_folder")

# ========== 修复2：下拉框滚动问题 ==========
print("\n[修复2] 修复下拉框滚动问题...")

# 找到并替换 bind_all 为 bind
old_mousewheel = '''        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)'''

new_mousewheel = '''        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)'''

if old_mousewheel in content:
    content = content.replace(old_mousewheel, new_mousewheel)
    print("  [OK] 已修复文案生成页面的滚动绑定")
else:
    print("  [FAIL] 未找到文案生成页面的滚动绑定")

# 保存修改后的文件
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("修复完成！")
print("="*50)
print("\n修复内容：")
print("1. 文件夹选择对话框现在会从当前路径开始")
print("2. 下拉框滚动时不会影响主页面滚动")
print("\n请重启程序查看效果。")
