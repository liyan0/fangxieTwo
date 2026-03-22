import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取文件
with open(r'D:\AIDownloadFiles\国学json\fangxie_tool.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在3295行后插入新的文风关键词库
insert_line = 3295  # 在"""后面插入

new_content = '''
        # 新增：文风关键词库（用于生成"安静/沉默"风格文案）
        style_keywords_protocol = """## 文风关键词库（增加多样性）

【安静沉默风格关键词】（约20%的文案使用此风格）
- 核心词：安静、沉默、不动如山、心如止水、以柔克刚
- 高级词：大象无形、深不见底、镇住场子、压轴、扫地僧
- 动作词：不说话、不解释、不辩解、不争辩、不表态
- 效果词：让他们慌了、让全场安静、让所有人心慌、镇住了全场

【使用场景】
- 当文案需要强调"你的沉稳"时使用
- 当文案需要对比"你的安静 VS 他们的慌乱"时使用
- 当文案需要体现"以柔克刚"、"不动如山"的境界时使用

【示例句式】
- "你越安静，他们越慌"
- "你一句话不说，全场都在等你表态"
- "你的沉默，比任何话都有分量"
- "你不动声色，他们已经坐不住了"
"""
'''

# 插入新内容
lines.insert(insert_line, new_content)

# 保存文件
with open(r'D:\AIDownloadFiles\国学json\fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ 新增文风关键词库成功')
print()
print('插入位置：第3295行之后')
print('内容：安静沉默风格关键词库')
