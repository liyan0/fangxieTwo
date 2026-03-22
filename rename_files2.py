# -*- coding: utf-8 -*-
import os

folder = r'D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案'
os.chdir(folder)

renames = {
    '上面那位发话了 那个老实人 我们必须留住.txt': '上面那位发话了，那个老实人，我们必须留住.txt',
    '他们低估了你的好 迟早要付出代价.txt': '他们低估了你的好，迟早要付出代价.txt',
    '他们傻眼了 以为你垮了 没想到你反击才刚开始.txt': '他们傻眼了，以为你垮了，没想到你反击才刚开始.txt',
    '你每退一步 他们就敢多进两步.txt': '你每退一步，他们就敢多进两步.txt',
    '大佬急了 他说那个一直沉默的人 深不见底.txt': '大佬急了，他说那个一直沉默的人，深不见底.txt',
    '完蛋了 你越安静 他们越慌神.txt': '完蛋了，你越安静，他们越慌神.txt',
    '有人急了 就因为你总说没事.txt': '有人急了，就因为你总说没事.txt',
    '有人背着你 悄悄给你记了一本账.txt': '有人背着你，悄悄给你记了一本账.txt',
    '注意了 那些人马上要后悔 你的好日子来了.txt': '注意了，那些人马上要后悔，你的好日子来了.txt',
    '炸锅了 那个从不争抢的人 竟然是最大的赢家.txt': '炸锅了，那个从不争抢的人，竟然是最大的赢家.txt',
    '紧急提醒 你再这样忍下去 真的要出问题了.txt': '紧急提醒，你再这样忍下去，真的要出问题了.txt',
    '说破了 你不是脾气好 你只是没人心疼.txt': '说破了，你不是脾气好，你只是没人心疼.txt',
}

for old, new in renames.items():
    if os.path.exists(old):
        os.rename(old, new)
        print(f'OK: {new}')
    else:
        print(f'未找到: {old}')

print('\n当前文件列表:')
for f in sorted(os.listdir('.')):
    print(f)
