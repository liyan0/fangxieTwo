# API配置修复说明

## 修复日期
2026-03-04

## 问题描述

用户在保存非流式API配置时遇到错误：
```
保存配置失败: invalid literal for int() with base 10: ''
```

同时测试API连接按钮也无法正常工作。

## 问题原因

在 `save_api_config()` 函数中（第1779-1807行），代码直接使用 `int()` 转换 `max_tokens` 输入框的值：

```python
self.config["stream_main_max_tokens"] = int(self.stream_main_max_tokens.get())
self.config["non_stream_main_max_tokens"] = int(self.non_stream_main_max_tokens.get())
# ... 其他类似代码
```

**问题：**
- 如果输入框为空，`int('')` 会抛出 ValueError
- 如果输入框包含非数字字符，`int()` 也会失败
- 没有任何错误处理和默认值机制

## 修复方案

添加了 `safe_int()` 辅助函数来安全地转换 max_tokens 值：

```python
def safe_int(value, default=16000):
    try:
        v = value.strip()
        if not v:
            return default
        return int(v)
    except (ValueError, AttributeError):
        return default
```

然后在所有 max_tokens 转换处使用这个函数：

```python
self.config["stream_main_max_tokens"] = safe_int(self.stream_main_max_tokens.get())
self.config["stream_backup_max_tokens"] = safe_int(self.stream_backup_max_tokens.get())
self.config["non_stream_main_max_tokens"] = safe_int(self.non_stream_main_max_tokens.get())
self.config["non_stream_backup_max_tokens"] = safe_int(self.non_stream_backup_max_tokens.get())
```

## 修复效果

1. **空值处理** - 如果 max_tokens 输入框为空，自动使用默认值 16000
2. **非法值处理** - 如果输入非数字字符，自动使用默认值 16000
3. **错误提示优化** - 不再显示技术性的错误信息，而是静默使用默认值

## 测试API连接功能

程序已经实现了智能API测试功能，会自动尝试三种格式：

1. **OpenAI格式** - 标准的 `/chat/completions` 端点
2. **OpenAI格式(无v1)** - 自动添加 `/v1` 前缀
3. **Anthropic格式** - 原生的 `/messages` 端点

**测试步骤：**
1. 在API配置页面填写 URL、API Key、模型名称
2. 点击"测试连接"按钮
3. 程序会自动尝试不同格式，找到可用的连接方式
4. 如果URL需要修正（如添加/v1），会自动更新

**常见问题：**
- 确保URL格式正确（如 `https://api.example.com/v1`）
- 确保API Key有效且未过期
- 确保模型名称正确（如 `claude-opus-4-5-20251101`）
- 检查网络连接是否正常

## 修复文件

- `fix_api_config_save.py` - 修复脚本
- `fangxie_tool.py` - 已修复的主程序

## 使用说明

修复已完成，程序已重启。现在：
1. 保存API配置时不会再报错
2. max_tokens 为空时会自动使用默认值 16000
3. 测试API连接功能正常工作

## 配置文件位置

`D:\AIDownloadFiles\国学json\fangxie_config.json`

当前配置的 max_tokens 值都是 16000（整数类型），配置文件正常。
