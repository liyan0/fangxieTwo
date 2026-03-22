# -*- coding: utf-8 -*-
"""
第二步：修改故事检测函数和提示词
"""

print("开始第二步修改...")

# 读取文件
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改has_story_opening函数，扩展检测词
old_story_markers = '''    def has_story_opening(self, result, article_count):
        """检测是否出现故事叙述式开场（仅检查每篇开头）"""
        story_markers = [
            "那天", "有一次", "后来我", "小时候", "当年",
            "我有个", "我认识", "我朋友", "有人问我", "有人跟我说"
        ]'''

new_story_markers = '''    def has_story_opening(self, result, article_count):
        """检测是否出现故事叙述式开场（仅检查每篇开头）- 扩展检测范围"""
        story_markers = [
            # 原有的故事标记
            "那天", "有一次", "后来我", "小时候", "当年",
            "我有个", "我认识", "我朋友", "有人问我", "有人跟我说",
            # 新增的故事场景标记
            "便利店", "地铁", "超市", "菜市场", "出租车", "司机", "老板娘",
            "邻居", "大妈", "大爷", "同事问", "朋友说", "我妈说", "我爸说",
            "我爷爷", "我奶奶", "我表姐", "我舅舅", "我发小", "我师傅",
            "单位有个", "公司有个", "小区", "茶水间", "电梯里", "咖啡店",
            "书店", "健身房", "高铁上", "邻座", "前几天", "昨天", "早上",
            "深夜", "参加", "去", "坐", "排队", "结账", "堵在路上",
            "我看到", "我听到", "我遇到", "有个人", "有人说"
        ]'''

content = content.replace(old_story_markers, new_story_markers)
print("已修改has_story_opening函数")

# 2. 修改检测到故事开头时的处理：从"仅提示不拦截"改为"需要重试"
old_story_check = '''        # 开头反故事化校验：命中故事触发词则重试
        if self.has_story_opening(result, article_count):
            self.log("检测到故事化开头（如"那天/有一次/有人问我"等），仅提示不拦截")'''

new_story_check = '''        # 开头反故事化校验：命中故事触发词则重试
        if self.has_story_opening(result, article_count):
            self.log("检测到故事化开头,需要重试...")
            return False'''

content = content.replace(old_story_check, new_story_check)
print("已修改故事检测拦截逻辑")

# 3. 修改get_random_hooks函数的注释
old_get_random = '''def get_random_hooks(count=3):
    """随机选择指定数量的不同类型开头，确保至少1个是轻松/温暖/反转类型"""
    light_types = ["A类-轻松幽默型", "B类-温暖治愈型", "C类-反转惊喜型"]'''

new_get_random = '''def get_random_hooks(count=3):
    """随机选择指定数量的不同类型开头，确保至少1个是宇宙天道/点醒直聊/身份认同类型"""
    light_types = ["A类-宇宙天道型", "B类-点醒直聊型", "C类-身份认同型"]'''

content = content.replace(old_get_random, new_get_random)
print("已修改get_random_hooks函数")

# 保存文件
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("第二步修改完成！")
