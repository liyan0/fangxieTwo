# -*- coding: utf-8 -*-
import openpyxl, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# 读取爆款标题库
wb = openpyxl.load_workbook(r'D:\A百家号标题库\百度标题采集\佛光护佑标题2.xlsx')
ws = wb.active
print('=== 爆款标题库 ===')
titles = []
for row in ws.iter_rows(min_row=2, values_only=True):
    t = str(row[0]) if row[0] else ''
    if t and t not in ('None', 'title'):
        titles.append(t)
print(f'共 {len(titles)} 条标题\n')
for i, t in enumerate(titles):
    print(f'{i+1}. {t}')

print('\n\n=== 我生成的标题（流量文案目录）===')
folder = r'D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案'
if os.path.exists(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    files.sort(reverse=True)
    print(f'共 {len(files)} 个文件，读取最新5个的标题：')
    for fname in files[:5]:
        fpath = os.path.join(folder, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # 提取标题行
        lines = content.split('\n')
        print(f'\n【{fname}】')
        for line in lines[:10]:
            if line.strip():
                print(f'  {line.strip()}')
else:
    print(f'目录不存在: {folder}')
