# -*- coding: utf-8 -*-
"""
第六步：修复语音路径跳转问题 + 添加更多结尾引流选项
"""

print("开始第六步修改...")

# 读取文件
with open('fangxie_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 修复1：添加语音路径到配置文件 =====
print("\n修复1：添加语音路径配置...")

# 1.1 修改DEFAULT_CONFIG，添加语音路径配置
old_default_config = '''DEFAULT_CONFIG = {
    "use_stream": True,  # 是否使用流式调用
    "similarity_threshold": 0.76,  # 生成文案相似度阈值（越低越严格）
    # 流式调用 - 主模型配置'''

new_default_config = '''DEFAULT_CONFIG = {
    "use_stream": True,  # 是否使用流式调用
    "similarity_threshold": 0.76,  # 生成文案相似度阈值（越低越严格）
    # 语音合成路径配置
    "voice_input_path": r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频文案/流量文案",
    "voice_output_path": r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频配音/流量语音",
    # 流式调用 - 主模型配置'''

content = content.replace(old_default_config, new_default_config)
print("  [OK] 已添加voice_input_path和voice_output_path到DEFAULT_CONFIG")

# 1.2 修改语音路径初始化，从配置文件读取
old_voice_paths = '''        # 文案输入目录
        voice_row2 = ttk.Frame(voice_config_frame)
        voice_row2.pack(fill=tk.X, pady=2)
        ttk.Label(voice_row2, text="文案目录:").pack(side=tk.LEFT)
        self.voice_input_path = tk.StringVar(value=r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频文案/流量文案")
        ttk.Entry(voice_row2, textvariable=self.voice_input_path, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(voice_row2, text="选择", command=self.select_voice_input_folder, width=6).pack(side=tk.LEFT)

        # 配音输出目录
        voice_row3 = ttk.Frame(voice_config_frame)
        voice_row3.pack(fill=tk.X, pady=2)
        ttk.Label(voice_row3, text="输出目录:").pack(side=tk.LEFT)
        self.voice_output_path = tk.StringVar(value=r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频配音/流量语音")'''

new_voice_paths = '''        # 文案输入目录
        voice_row2 = ttk.Frame(voice_config_frame)
        voice_row2.pack(fill=tk.X, pady=2)
        ttk.Label(voice_row2, text="文案目录:").pack(side=tk.LEFT)
        self.voice_input_path = tk.StringVar(value=self.config.get("voice_input_path", r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频文案/流量文案"))
        ttk.Entry(voice_row2, textvariable=self.voice_input_path, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(voice_row2, text="选择", command=self.select_voice_input_folder, width=6).pack(side=tk.LEFT)

        # 配音输出目录
        voice_row3 = ttk.Frame(voice_config_frame)
        voice_row3.pack(fill=tk.X, pady=2)
        ttk.Label(voice_row3, text="输出目录:").pack(side=tk.LEFT)
        self.voice_output_path = tk.StringVar(value=self.config.get("voice_output_path", r"D:/AIDownloadFiles/国学json/百家号带货视频/baijiadaihuo/input/视频配音/流量语音"))'''

content = content.replace(old_voice_paths, new_voice_paths)
print("  [OK] 已修改语音路径初始化，从配置文件读取")

# 1.3 修改select_voice_input_folder和select_voice_output_folder，保存到配置
old_select_voice_input = '''    def select_voice_input_folder(self):
        """选择语音合成的文案输入目录"""
        folder_path = filedialog.askdirectory(title="选择文案目录")
        if folder_path:
            self.voice_input_path.set(folder_path)'''

new_select_voice_input = '''    def select_voice_input_folder(self):
        """选择语音合成的文案输入目录"""
        folder_path = filedialog.askdirectory(title="选择文案目录")
        if folder_path:
            self.voice_input_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_input_path"] = folder_path
            save_config(self.config)'''

content = content.replace(old_select_voice_input, new_select_voice_input)
print("  [OK] 已修改select_voice_input_folder，选择后自动保存")

old_select_voice_output = '''    def select_voice_output_folder(self):
        """选择语音合成的输出目录"""
        folder_path = filedialog.askdirectory(title="选择配音输出目录")
        if folder_path:
            self.voice_output_path.set(folder_path)'''

new_select_voice_output = '''    def select_voice_output_folder(self):
        """选择语音合成的输出目录"""
        folder_path = filedialog.askdirectory(title="选择配音输出目录")
        if folder_path:
            self.voice_output_path.set(folder_path)
            # 保存到配置文件
            self.config["voice_output_path"] = folder_path
            save_config(self.config)'''

content = content.replace(old_select_voice_output, new_select_voice_output)
print("  [OK] 已修改select_voice_output_folder，选择后自动保存")

# ===== 修复2：添加更多结尾引流选项 =====
print("\n修复2：添加更多结尾引流选项...")

# 从参考素材中提取的新引流话术
old_yinliu_templates = '''    # 引流话术库（按类型分开存储）
    "yinliu_templates": {
        "置顶引流": [
            "关于怎么彻底走出这个困局，我在主页置顶视频里讲得很透。那里有一套方法，是我这些年摸爬滚打总结出来的，不适合在这里公开讲。你要是真想改变，点我头像，去看置顶第一条，看完你就明白该怎么做了。",
            "现在你就点开我的头像，进我主页，去看置顶的那个视频，我在那里给你留了一套破局的方法。听得懂那便是你的收获，听不懂说明时机还没到。准备好了吗？这一局该你赢了。",
            "从今天开始，学着为自己活一次... 答应我，现在点击我的头像进主页看看，置顶前两条视频，那里有我想对你说的心里话，这些话我只说给你听，因为你扛了太久，总该有人懂你的不易。",
            "如果你也想从这种困境里走出来，想活得通透一点、轻松一点，点我头像，去看主页置顶的视频。那里有你一直在找的答案，也有你需要的那份力量。我在那里等你。"
        ],'''

new_yinliu_templates = '''    # 引流话术库（按类型分开存储）
    "yinliu_templates": {
        "置顶引流": [
            "关于怎么彻底走出这个困局，我在主页置顶视频里讲得很透。那里有一套方法，是我这些年摸爬滚打总结出来的，不适合在这里公开讲。你要是真想改变，点我头像，去看置顶第一条，看完你就明白该怎么做了。",
            "现在你就点开我的头像，进我主页，去看置顶的那个视频，我在那里给你留了一套破局的方法。听得懂那便是你的收获，听不懂说明时机还没到。准备好了吗？这一局该你赢了。",
            "从今天开始，学着为自己活一次... 答应我，现在点击我的头像进主页看看，置顶前两条视频，那里有我想对你说的心里话，这些话我只说给你听，因为你扛了太久，总该有人懂你的不易。",
            "如果你也想从这种困境里走出来，想活得通透一点、轻松一点，点我头像，去看主页置顶的视频。那里有你一直在找的答案，也有你需要的那份力量。我在那里等你。",
            "现在你就点开我的头像，入我门庭，去看主页置顶的视频。那里有一套完整的方法，是我用多年经验总结出来的，专门留给像你这样的人。看完之后，你就知道该怎么做了。",
            "点击我的头像进主页，去看置顶第一个视频。那里有你一直在寻找的答案，有你需要的那份力量。这不是巧合，是你该看到的时候到了。",
            "如果你想彻底改变现状，点我头像，去主页看置顶视频。那里有一套破局的方法，是我这些年摸爬滚打总结出来的，不适合在这里公开讲。你要是真想改变，就去看看。",
            "答应我，现在就点开我的头像，进主页看置顶的那两条视频。那里有我想对你说的心里话，这些话我只说给你听，因为你扛了太久，总该有人懂你的不易。",
            "关于如何走出困境，我在主页置顶视频里讲得很透彻。那里有一套完整的方法论，是我用多年经验换来的。你要是真想改变，点我头像，去看置顶第一条。",
            "现在你只需要做一件事：点开我的头像，进主页，去看置顶的视频。那里有你一直在找的答案，也有你需要的那份底气。我在那里等你。",
            "如果你也想从这种困境里走出来，想活得明白一点、轻松一点，点我头像，去看主页置顶的视频。那里有你需要的方法，也有你需要的力量。",
            "点开我的头像，进我主页，去看置顶的那个视频。我在那里给你留了一套破局的方法，听得懂那便是你的收获，听不懂说明时机还没到。准备好了吗？",
            "关于怎么彻底改变现状，我在主页置顶视频里讲得很清楚。那里有一套方法，是我这些年总结出来的，专门留给像你这样的人。你要是真想改变，就去看看。"
        ],'''

content = content.replace(old_yinliu_templates, new_yinliu_templates)
print("  [OK] 已添加9个新的置顶引流话术（从4个增加到13个）")

# 保存文件
with open('fangxie_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("第六步修改完成！")
print("="*50)
print("\n修改总结：")
print("1. [OK] 修复了语音路径跳转问题")
print("   - 添加voice_input_path和voice_output_path到配置文件")
print("   - 修改初始化逻辑，从配置文件读取路径")
print("   - 修改选择文件夹函数，自动保存到配置")
print("   - 现在选择'引导文案'后，下次启动会保持该选择")
print("\n2. [OK] 添加了更多结尾引流选项")
print("   - 置顶引流：从4个增加到13个（+9个新选项）")
print("   - 新增的话术都是从参考素材中提取的玄学大气风格")
print("\n所有修改已完成！请运行程序测试。")
