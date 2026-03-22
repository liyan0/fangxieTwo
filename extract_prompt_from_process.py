# -*- coding: utf-8 -*-
"""
从正在运行的进程中提取 build_prompt 方法的源代码
"""
import ctypes
import struct
import sys

def read_process_memory(pid):
    """尝试读取进程内存"""
    # Windows API
    PROCESS_VM_READ = 0x0010
    PROCESS_QUERY_INFORMATION = 0x0400

    kernel32 = ctypes.windll.kernel32

    # 打开进程
    handle = kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)

    if not handle:
        print(f"无法打开进程 {pid}")
        return None

    print(f"成功打开进程 {pid}, 句柄: {handle}")

    # 尝试搜索特定字符串
    search_strings = [
        b"build_prompt",
        b"def build_prompt",
        b"voice_combo",
        b"explosive_content_protocol",
        b"title_explosive_protocol"
    ]

    # 读取内存区域
    # 注意：这需要知道内存地址，比较复杂

    kernel32.CloseHandle(handle)
    return None

if __name__ == "__main__":
    pid = 73688
    print("=" * 60)
    print("尝试从进程中提取提示词...")
    print("=" * 60)

    # 方法：通过 Windows 调试 API
    # 这需要管理员权限

    result = read_process_memory(pid)

    if result:
        print("提取成功！")
        print(result)
    else:
        print("\n直接读取内存失败。")
        print("\n建议方案：")
        print("1. 在正在运行的程序中，点击'生成流量文案'")
        print("2. 查看日志输出，看是否有提示词相关信息")
        print("3. 或者告诉我：生成的文案有什么特征（标题格式、内容风格等）")
        print("   我可以通过特征反推出使用的提示词版本")
