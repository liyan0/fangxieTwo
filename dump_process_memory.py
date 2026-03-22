# -*- coding: utf-8 -*-
"""
尝试从正在运行的Python进程中提取源代码
"""
import sys
import os

# 连接到目标进程
target_pid = 73688

print(f"尝试连接到进程 {target_pid}...")

# 方法1: 尝试通过pyrasite注入代码
try:
    import pyrasite
    print("使用 pyrasite 方法...")

    # 创建注入代码
    inject_code = """
import sys
import inspect

# 查找 FangxieApp 类
for name, obj in sys.modules.items():
    if hasattr(obj, 'FangxieApp'):
        print(f"找到模块: {name}")
        # 获取类的源代码
        try:
            source = inspect.getsource(obj.FangxieApp)
            print("=" * 50)
            print("FangxieApp 类源代码:")
            print("=" * 50)
            print(source[:2000])  # 打印前2000字符
        except:
            pass

        # 查找 voice_combo 相关代码
        if hasattr(obj.FangxieApp, '__init__'):
            try:
                init_source = inspect.getsource(obj.FangxieApp.__init__)
                # 查找音色相关的行
                for line in init_source.split('\\n'):
                    if 'voice' in line.lower() or '音色' in line:
                        print(line)
            except:
                pass
"""

    # 注入并执行
    shell = pyrasite.PyrasiteIPC(target_pid)
    shell.connect()
    result = shell.cmd(inject_code)
    print(result)

except ImportError:
    print("pyrasite 未安装")
except Exception as e:
    print(f"pyrasite 方法失败: {e}")

# 方法2: 使用 gdb (如果在Linux上)
print("\n尝试其他方法...")

# 方法3: 读取 /proc/pid/maps 和内存 (Linux)
# Windows上需要用其他方法

print("Windows系统，尝试使用 ctypes 读取内存...")
