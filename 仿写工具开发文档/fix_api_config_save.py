# -*- coding: utf-8 -*-
"""
修复API配置保存时的int转换错误
"""

import os

# 读取文件
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("开始修复API配置保存问题...")

# 修复save_api_config函数，添加错误处理和默认值
old_save_function = '''    def save_api_config(self):
        """保存API配置"""
        try:
            self.config["use_stream"] = self.use_stream.get()
            threshold_value = self._parse_similarity_threshold()
            self.config["similarity_threshold"] = threshold_value
            self.similarity_threshold = threshold_value
            # 流式配置
            self.config["stream_main_url"] = self.stream_main_url.get().strip()
            self.config["stream_main_key"] = self.stream_main_key.get().strip()
            self.config["stream_main_model"] = self.stream_main_model.get().strip()
            self.config["stream_main_max_tokens"] = int(self.stream_main_max_tokens.get())
            self.config["stream_backup_url"] = self.stream_backup_url.get().strip()
            self.config["stream_backup_key"] = self.stream_backup_key.get().strip()
            self.config["stream_backup_model"] = self.stream_backup_model.get().strip()
            self.config["stream_backup_max_tokens"] = int(self.stream_backup_max_tokens.get())
            # 非流式配置
            self.config["non_stream_main_url"] = self.non_stream_main_url.get().strip()
            self.config["non_stream_main_key"] = self.non_stream_main_key.get().strip()
            self.config["non_stream_main_model"] = self.non_stream_main_model.get().strip()
            self.config["non_stream_main_max_tokens"] = int(self.non_stream_main_max_tokens.get())
            self.config["non_stream_backup_url"] = self.non_stream_backup_url.get().strip()
            self.config["non_stream_backup_key"] = self.non_stream_backup_key.get().strip()
            self.config["non_stream_backup_model"] = self.non_stream_backup_model.get().strip()
            self.config["non_stream_backup_max_tokens"] = int(self.non_stream_backup_max_tokens.get())
            save_config(self.config)
            messagebox.showinfo("成功", "API配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{e}")'''

new_save_function = '''    def save_api_config(self):
        """保存API配置"""
        try:
            self.config["use_stream"] = self.use_stream.get()
            threshold_value = self._parse_similarity_threshold()
            self.config["similarity_threshold"] = threshold_value
            self.similarity_threshold = threshold_value

            # 辅助函数：安全转换max_tokens
            def safe_int(value, default=16000):
                try:
                    v = value.strip()
                    if not v:
                        return default
                    return int(v)
                except (ValueError, AttributeError):
                    return default

            # 流式配置
            self.config["stream_main_url"] = self.stream_main_url.get().strip()
            self.config["stream_main_key"] = self.stream_main_key.get().strip()
            self.config["stream_main_model"] = self.stream_main_model.get().strip()
            self.config["stream_main_max_tokens"] = safe_int(self.stream_main_max_tokens.get())
            self.config["stream_backup_url"] = self.stream_backup_url.get().strip()
            self.config["stream_backup_key"] = self.stream_backup_key.get().strip()
            self.config["stream_backup_model"] = self.stream_backup_model.get().strip()
            self.config["stream_backup_max_tokens"] = safe_int(self.stream_backup_max_tokens.get())
            # 非流式配置
            self.config["non_stream_main_url"] = self.non_stream_main_url.get().strip()
            self.config["non_stream_main_key"] = self.non_stream_main_key.get().strip()
            self.config["non_stream_main_model"] = self.non_stream_main_model.get().strip()
            self.config["non_stream_main_max_tokens"] = safe_int(self.non_stream_main_max_tokens.get())
            self.config["non_stream_backup_url"] = self.non_stream_backup_url.get().strip()
            self.config["non_stream_backup_key"] = self.non_stream_backup_key.get().strip()
            self.config["non_stream_backup_model"] = self.non_stream_backup_model.get().strip()
            self.config["non_stream_backup_max_tokens"] = safe_int(self.non_stream_backup_max_tokens.get())
            save_config(self.config)
            messagebox.showinfo("成功", "API配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{e}")'''

if old_save_function in content:
    content = content.replace(old_save_function, new_save_function)
    print("  [OK] 已修复 save_api_config 函数")
else:
    print("  [FAIL] 未找到 save_api_config 函数")

# 保存修改后的文件
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("修复完成！")
print("="*50)
print("\n修复内容：")
print("1. 添加了 safe_int() 辅助函数处理max_tokens转换")
print("2. 空值或非法值会使用默认值16000")
print("3. 避免了 'invalid literal for int()' 错误")
print("\n请重启程序测试。")
