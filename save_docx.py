# -*- coding: utf-8 -*-
import os
import sys
from docx import Document
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 读取文案内容
with open(r'D:\AIDownloadFiles\国学json\wenan_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 创建文档
doc = Document()

# 按行添加内容
for line in content.split('\n'):
    doc.add_paragraph(line)

# 保存到指定目录
today = datetime.now().strftime('%Y%m%d')
save_dir = 'D:\\A百家号带货视频\\带货文案'

# 使用pathlib处理中文路径
from pathlib import Path
save_path = Path(save_dir)
save_path.mkdir(parents=True, exist_ok=True)

filepath = save_path / f'{today}_文案1.docx'
doc.save(str(filepath))
print(f'已保存: {filepath}')
