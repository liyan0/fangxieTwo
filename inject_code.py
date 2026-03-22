# -*- coding: utf-8 -*-
"""
注入代码到正在运行的进程，让它输出 build_prompt 方法
"""
import socket
import sys

# 创建一个简单的注入脚本
injection_code = """
import inspect
import sys

# 查找 FangxieApp 类
app_instance = None
for obj in gc.get_objects():
    if type(obj).__name__ == 'FangxieApp':
        app_instance = obj
        break

if app_instance:
    # 获取 build_prompt 方法的源代码
    try:
        method = getattr(app_instance, 'build_prompt', None)
        if method:
            source = inspect.getsource(method)

            # 保存到文件
            with open('D:/AIDownloadFiles/国学json/extracted_build_prompt.txt', 'w', encoding='utf-8') as f:
                f.write("=" * 60)
                f.write("\\n从运行进程中提取的 build_prompt 方法\\n")
                f.write("=" * 60)
                f.write("\\n\\n")
                f.write(source)

            print("提示词已保存到: extracted_build_prompt.txt")
    except Exception as e:
        print(f"提取失败: {e}")
else:
    print("未找到 FangxieApp 实例")
"""

print("=" * 60)
print("方案：通过 Python 调试端口注入代码")
print("=" * 60)
print()
print("由于 Windows 限制，直接注入很困难。")
print()
print("更简单的方法：")
print("1. 在正在运行的程序窗口中，打开 Python 控制台（如果有）")
print("2. 或者在程序的日志区域，看看能否找到提示词的痕迹")
print("3. 或者生成一篇文案，我通过文案的特征来反推提示词")
print()
print("你能否：")
print("- 用正在运行的程序生成一篇文案")
print("- 把生成的文案内容发给我")
print("- 我通过分析文案的结构、风格、标题格式等")
print("- 就能知道使用的是哪个版本的提示词")
