
import sys
import os

# 尝试获取fangxie_tool模块的源代码
output_file = r'D:\AIDownloadFiles\国学jsonangxie_tool_from_running.py'

try:
    # 方法1: 如果模块已加载，从__main__获取
    if hasattr(sys.modules.get('__main__'), '__file__'):
        main_file = sys.modules['__main__'].__file__
        if main_file and 'fangxie_tool' in main_file:
            with open(main_file, 'r', encoding='utf-8') as f:
                source = f.read()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(source)
            print(f"SUCCESS: Saved to {output_file}")
        else:
            print(f"Main file: {main_file}")
    
    # 方法2: 列出所有已加载的模块
    print("
Loaded modules containing 'fangxie':")
    for name, module in sys.modules.items():
        if 'fangxie' in name.lower():
            print(f"  {name}: {getattr(module, '__file__', 'no file')}")
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
