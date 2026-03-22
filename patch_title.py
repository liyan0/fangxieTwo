# -*- coding: utf-8 -*-
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines[4222] = '**【公式5：你被选中/认可型】** 大佬/高人看上你了\n'
lines[4223] = '- 结构：[大佬/高人/有缘人] + [对你的认可/行动]\n'
lines[4224] = '- 爆款参考：\"大佬想给你一张通行证\"\n'
lines[4225] = '- 爆款参考：\"大佬当众为你撑腰\"\n'
lines[4226] = '- 爆款参考：\"他谁都看不上 但偏偏对你特别欣赏\"\n'
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('修改完成')
