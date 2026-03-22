# UI问题修复说明

## 修复日期
2026-03-04

## 修复的问题

### 问题1：文件夹选择对话框跳转错误
**问题描述**：
- 点击"流量文案保存路径"旁边的"选择文件夹"按钮时，对话框不会从当前路径开始
- 点击"语音合成配置"的"文案目录"和"输出目录"旁边的"选择"按钮时，也不会从当前路径开始
- 导致每次都要从默认位置重新导航

**修复方案**：
为以下三个函数添加 `initialdir` 参数，使用输入框中的当前路径作为初始目录：
- `select_txt_output_folder()` - 流量文案保存路径
- `select_voice_input_folder()` - 语音合成文案目录
- `select_voice_output_folder()` - 语音合成输出目录

**修复代码示例**：
```python
def select_txt_output_folder(self):
    """选择TXT保存文件夹"""
    current_path = self.txt_output_path.get()
    initial_dir = current_path if current_path and os.path.exists(current_path) else None
    folder_path = filedialog.askdirectory(title="选择TXT保存文件夹", initialdir=initial_dir)
    if folder_path:
        self.txt_output_path.set(folder_path)
```

### 问题2：下拉框滚动时主页面也滚动
**问题描述**：
- 在"引流话术（可选）"下拉框中，双击展开后上下滚动时
- 主页面也会跟着一起滚动
- 下拉框本身不动，导致操作不便

**原因分析**：
代码中使用了 `canvas.bind_all("<MouseWheel>", _on_mousewheel)`，这会将鼠标滚轮事件绑定到所有控件，包括Combobox的下拉列表。

**修复方案**：
将 `bind_all` 改为 `bind`，只绑定到Canvas和scrollable_frame，不影响其他控件：

```python
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind("<MouseWheel>", _on_mousewheel)
scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
```

### 问题3：配置保存说明
**用户疑问**：页面上的修改是否实时保存？保存在哪个配置文件里？

**说明**：
1. **语音路径配置**：
   - 选择"文案目录"或"输出目录"后会**立即保存**到配置文件
   - 代码中有 `save_config(self.config)` 调用

2. **引流话术配置**：
   - 在"引流话术（可选）"中添加、删除话术后会**立即保存**
   - `save_yinliu_template()` 和 `delete_yinliu_template()` 都会调用 `save_config()`

3. **API配置**：
   - 需要在"API配置"页面点击"保存配置"按钮才会保存
   - 包括：流式/非流式切换、API地址、密钥、模型名称、相似度阈值等

4. **配置文件位置**：
   - `D:\AIDownloadFiles\国学json\fangxie_config.json`
   - 程序启动时会自动加载此文件
   - 如果文件不存在，会从代码中的 `DEFAULT_CONFIG` 生成

## 修复文件
- `fix_ui_issues.py` - 修复脚本
- `fangxie_tool.py` - 已修复的主程序

## 测试验证
修复后需要测试：
1. 点击各个"选择文件夹"按钮，确认对话框从当前路径开始
2. 展开引流话术下拉框，滚动时确认主页面不会跟着滚动
3. 修改配置后检查 `fangxie_config.json` 文件内容

## 使用说明
修复已完成，程序已重启。现在：
- 文件夹选择对话框会从输入框中的路径开始
- 下拉框滚动不会影响主页面
- 配置会根据操作类型自动或手动保存
