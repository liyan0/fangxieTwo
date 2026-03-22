# -*- coding: utf-8 -*-
import os

folder = r'D:\AIDownloadFiles\国学json\百家号带货视频\baijiadaihuo\input\视频文案\流量文案'
os.chdir(folder)

renames = {
    '那个总说\u201c没事\u201d的你，有人心疼了.txt': '有人急了 就因为你总说没事.txt',
    '有人背着你，把你的福泽记在了账上.txt': '有人背着你 悄悄给你记了一本账.txt',
    '你越安静，身边人越是坐不住了.txt': '完蛋了 你越安静 他们越慌神.txt',
    '你的福泽在后头，那些人马上要后悔了.txt': '注意了 那些人马上要后悔 你的好日子来了.txt',
    '你的好，值得被好好珍惜.txt': '他们低估了你的好 迟早要付出代价.txt',
    '你再这样下去，这辈子就真的废了.txt': '紧急提醒 你再这样忍下去 真的要出问题了.txt',
    '你不是脾气好，你只是习惯了不被人心疼.txt': '说破了 你不是脾气好 你只是没人心疼.txt',
    '你一退再退，他们就敢步步紧逼.txt': '你每退一步 他们就敢多进两步.txt',
    '他们以为你垮了，其实你的反击才刚开始.txt': '他们傻眼了 以为你垮了 没想到你反击才刚开始.txt',
}

for old, new in renames.items():
    if os.path.exists(old):
        os.rename(old, new)
        print(f'OK: {old} -> {new}')
    else:
        print(f'NOT FOUND: {old}')

print('\n当前文件列表:')
for f in sorted(os.listdir('.')):
    print(f)
