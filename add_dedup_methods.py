import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取文件
with open(r'D:\AIDownloadFiles\国学json\fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在get_generated_title_set方法后添加标题去重方法
new_method_1 = '''
    def check_title_duplicate(self, title, threshold=0.7):
        """检查标题是否与历史标题重复"""
        from difflib import SequenceMatcher

        # 获取历史标题集合
        historical_titles = self.get_generated_title_set()

        if not historical_titles:
            return False

        # 计算与每个历史标题的相似度
        for hist_title in historical_titles:
            similarity = SequenceMatcher(None, title, hist_title).ratio()
            if similarity >= threshold:
                self.log(f"  ⚠️ 标题重复（相似度{similarity:.2%}）: {title}")
                self.log(f"     与历史标题: {hist_title}")
                return True

        return False
'''

# 查找插入位置（在get_generated_title_set方法后）
insert_pos = content.find('    def append_generated_to_library(self, flow_type, title, article_content):')
if insert_pos > 0:
    content = content[:insert_pos] + new_method_1 + '\n' + content[insert_pos:]
    print('✅ 添加标题去重方法 check_title_duplicate')
else:
    print('❌ 未找到插入位置1')

# 2. 添加参考文章去重方法（在check_title_duplicate后）
new_method_2 = '''
    def check_reference_duplicate(self, reference_content, threshold=0.8):
        """检查参考文章是否已在爆款素材库中"""
        from difflib import SequenceMatcher
        import openpyxl

        try:
            if not os.path.exists(MATERIAL_LIBRARY_FILE):
                return False

            wb = openpyxl.load_workbook(MATERIAL_LIBRARY_FILE, read_only=True)
            ws = wb.active

            # 读取爆款素材库中的所有文章
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or len(row) < 3:
                    continue

                material_content = str(row[2] or "").strip()  # 第3列是正文
                if not material_content:
                    continue

                # 计算相似度
                similarity = SequenceMatcher(None, reference_content[:500], material_content[:500]).ratio()
                if similarity >= threshold:
                    self.log(f"  ⚠️ 参考文章重复（相似度{similarity:.2%}），跳过改写")
                    wb.close()
                    return True

            wb.close()
            return False

        except Exception as e:
            self.log(f"  检查参考文章去重失败: {str(e)}")
            return False
'''

# 查找插入位置（在check_title_duplicate方法后）
insert_pos2 = content.find('    def append_generated_to_library(self, flow_type, title, article_content):')
if insert_pos2 > 0:
    content = content[:insert_pos2] + new_method_2 + '\n' + content[insert_pos2:]
    print('✅ 添加参考文章去重方法 check_reference_duplicate')
else:
    print('❌ 未找到插入位置2')

# 保存文件
with open(r'D:\AIDownloadFiles\国学json\fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print()
print('去重方法添加完成')
