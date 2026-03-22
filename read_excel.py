import pandas as pd
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取Excel文件前60条
df = pd.read_excel('D:/A百家号带货视频/带货文案/爆款参考文案/爆款素材库.xlsx', nrows=60)

print('列名:', df.columns.tolist())
print('\n总共读取了', len(df), '条数据\n')

# 显示前10条
for i in range(min(10, len(df))):
    print(f'\n===== 第{i+1}条 =====')
    for col in df.columns:
        val = str(df.iloc[i][col])
        if len(val) > 500:
            val = val[:500] + '...'
        print(f'{col}: {val}')
