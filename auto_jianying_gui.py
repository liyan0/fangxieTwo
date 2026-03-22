# -*- coding: utf-8 -*-
"""
剪映自动化工具 - GUI版本
功能：自动化剪映操作，包括导入素材、生成字幕、导出视频
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
import time
import random
from datetime import datetime

# 配置文件
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "jianying_config.json")

DEFAULT_CONFIG = {
    "jianying_path": r"D:\A压缩文件\剪映5.9版本免激活\JianyingPro\JianyingPro.exe",
    "video_source_path": r"D:\BaiduNetdiskDownload\自然风景视频素材",
    "audio_source_path": r"D:\A百家号带货视频\A带货配音",
    "export_path": r"D:\A百家号带货视频\A剪映视频",
    "bgm_path": r"D:\A百家号带货视频\BGM",
    "videos_per_folder": 3,
    "subtitle_style": {
        "font_size": "36",
        "font_family": "微软雅黑",
        "color": "金色",
    },
    "enable_bgm": True,
    "enable_effect": True,
    "coords": {
        "start_create": {"x": 0, "y": 0, "desc": "开始制作按钮"},
        "import_btn": {"x": 0, "y": 0, "desc": "导入按钮"},
        "add_to_track": {"x": 0, "y": 0, "desc": "添加到轨道(+号)"},
        "text_menu": {"x": 0, "y": 0, "desc": "文本菜单"},
        "smart_subtitle": {"x": 0, "y": 0, "desc": "智能字幕"},
        "start_recognize": {"x": 0, "y": 0, "desc": "开始识别"},
        "subtitle_select_all": {"x": 0, "y": 0, "desc": "字幕全选"},
        "subtitle_style_btn": {"x": 0, "y": 0, "desc": "字幕样式按钮"},
        "font_family_input": {"x": 0, "y": 0, "desc": "字体输入框"},
        "font_size_input": {"x": 0, "y": 0, "desc": "字号输入框"},
        "font_color_btn": {"x": 0, "y": 0, "desc": "字体颜色按钮"},
        "color_gold": {"x": 0, "y": 0, "desc": "金色选项"},
        "audio_menu": {"x": 0, "y": 0, "desc": "音频菜单"},
        "audio_import": {"x": 0, "y": 0, "desc": "音频导入"},
        "effect_menu": {"x": 0, "y": 0, "desc": "特效菜单"},
        "effect_select": {"x": 0, "y": 0, "desc": "选择特效"},
        "effect_apply": {"x": 0, "y": 0, "desc": "应用特效"},
        "export_btn": {"x": 0, "y": 0, "desc": "导出按钮"},
        "export_confirm": {"x": 0, "y": 0, "desc": "确认导出"},
    }
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                # Merge nested defaults for backward compatibility.
                if "subtitle_style" not in config or not isinstance(config["subtitle_style"], dict):
                    config["subtitle_style"] = DEFAULT_CONFIG["subtitle_style"].copy()
                else:
                    for k, v in DEFAULT_CONFIG["subtitle_style"].items():
                        config["subtitle_style"].setdefault(k, v)

                if "coords" not in config or not isinstance(config["coords"], dict):
                    config["coords"] = DEFAULT_CONFIG["coords"].copy()
                else:
                    for k, v in DEFAULT_CONFIG["coords"].items():
                        config["coords"].setdefault(k, v)
                return config
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

class JianyingAutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("剪映自动化工具")
        self.root.geometry("900x700")
        self.config = load_config()
        self.is_running = False
        self.measuring = False
        self.available_fonts = self.detect_available_fonts()

        self.create_widgets()
        self.start_position_tracker()

    def detect_available_fonts(self):
        """Detect locally available subtitle fonts and return display->search_name mapping."""
        candidates = [
            ("微软雅黑", "微软雅黑", ["msyh.ttc", "msyhbd.ttc"]),
            ("黑体", "黑体", ["simhei.ttf"]),
            ("宋体", "宋体", ["simsun.ttc"]),
            ("楷体", "楷体", ["simkai.ttf", "Kaiu.ttf"]),
            ("仿宋", "仿宋", ["simfang.ttf"]),
            ("等线", "等线", ["Deng.ttf", "Dengb.ttf"]),
        ]
        fonts_dir = r"C:\Windows\Fonts"
        available = {}
        for label, search_name, files in candidates:
            if any(os.path.exists(os.path.join(fonts_dir, f)) for f in files):
                available[label] = search_name
        # Ensure at least one option.
        if not available:
            available["微软雅黑"] = "微软雅黑"
        return available

    def get_selected_font_search_name(self):
        label = self.subtitle_font.get() if hasattr(self, "subtitle_font") else "微软雅黑"
        return self.available_fonts.get(label, label)

    def create_widgets(self):
        # 创建Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 标签页1：主操作
        self.main_page = ttk.Frame(self.notebook)
        self.notebook.add(self.main_page, text="  视频制作  ")
        self.create_main_page()

        # 标签页2：坐标设置
        self.coord_page = ttk.Frame(self.notebook)
        self.notebook.add(self.coord_page, text="  坐标设置  ")
        self.create_coord_page()

        # 标签页3：路径配置
        self.config_page = ttk.Frame(self.notebook)
        self.notebook.add(self.config_page, text="  路径配置  ")
        self.create_config_page()

    def create_main_page(self):
        main_frame = ttk.Frame(self.main_page, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 音频选择
        audio_frame = ttk.LabelFrame(main_frame, text="1. 选择配音文件", padding="10")
        audio_frame.pack(fill=tk.X, pady=5)

        self.audio_path = tk.StringVar()
        ttk.Entry(audio_frame, textvariable=self.audio_path, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(audio_frame, text="选择文件", command=self.select_audio, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(audio_frame, text="从列表选", command=self.show_audio_list, width=10).pack(side=tk.LEFT)

        # 视频素材设置
        video_frame = ttk.LabelFrame(main_frame, text="2. 视频素材设置", padding="10")
        video_frame.pack(fill=tk.X, pady=5)

        row1 = ttk.Frame(video_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="素材文件夹:").pack(side=tk.LEFT)
        self.video_source = tk.StringVar(value=self.config["video_source_path"])
        ttk.Entry(row1, textvariable=self.video_source, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1, text="选择", command=self.select_video_folder, width=6).pack(side=tk.LEFT)

        row2 = ttk.Frame(video_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="每文件夹取:").pack(side=tk.LEFT)
        self.videos_per_folder = tk.StringVar(value=str(self.config["videos_per_folder"]))
        ttk.Combobox(row2, textvariable=self.videos_per_folder, width=5,
                    values=["1","2","3","4","5"]).pack(side=tk.LEFT, padx=5)
        ttk.Label(row2, text="个视频").pack(side=tk.LEFT)

        # 字幕样式设置
        subtitle_frame = ttk.LabelFrame(main_frame, text="3. 字幕样式", padding="10")
        subtitle_frame.pack(fill=tk.X, pady=5)

        sub_row = ttk.Frame(subtitle_frame)
        sub_row.pack(fill=tk.X, pady=2)
        ttk.Label(sub_row, text="字体:").pack(side=tk.LEFT)
        default_font = self.config.get("subtitle_style", {}).get("font_family", "微软雅黑")
        if default_font not in self.available_fonts:
            default_font = next(iter(self.available_fonts.keys()))
        self.subtitle_font = tk.StringVar(value=default_font)
        ttk.Combobox(
            sub_row,
            textvariable=self.subtitle_font,
            width=10,
            values=list(self.available_fonts.keys()),
            state="readonly"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(sub_row, text="字号:").pack(side=tk.LEFT)
        self.subtitle_size = tk.StringVar(value=self.config.get("subtitle_style", {}).get("font_size", "36"))
        ttk.Combobox(sub_row, textvariable=self.subtitle_size, width=6,
                    values=["24","28","32","36","40","48","56"]).pack(side=tk.LEFT, padx=5)

        ttk.Label(sub_row, text="颜色:").pack(side=tk.LEFT, padx=(15,0))
        self.subtitle_color = tk.StringVar(value=self.config.get("subtitle_style", {}).get("color", "金色"))
        ttk.Combobox(sub_row, textvariable=self.subtitle_color, width=8,
                    values=["金色","黄色","白色","红色"]).pack(side=tk.LEFT, padx=5)

        # 背景音乐设置
        bgm_frame = ttk.LabelFrame(main_frame, text="4. 背景音乐", padding="10")
        bgm_frame.pack(fill=tk.X, pady=5)

        bgm_row1 = ttk.Frame(bgm_frame)
        bgm_row1.pack(fill=tk.X, pady=2)
        self.enable_bgm = tk.BooleanVar(value=self.config.get("enable_bgm", True))
        ttk.Checkbutton(bgm_row1, text="添加背景音乐", variable=self.enable_bgm).pack(side=tk.LEFT)

        bgm_row2 = ttk.Frame(bgm_frame)
        bgm_row2.pack(fill=tk.X, pady=2)
        ttk.Label(bgm_row2, text="BGM文件夹:").pack(side=tk.LEFT)
        self.bgm_path = tk.StringVar(value=self.config.get("bgm_path", ""))
        ttk.Entry(bgm_row2, textvariable=self.bgm_path, width=45).pack(side=tk.LEFT, padx=5)
        ttk.Button(bgm_row2, text="选择", command=self.select_bgm_folder, width=6).pack(side=tk.LEFT)

        # 特效设置
        effect_frame = ttk.LabelFrame(main_frame, text="5. 特效", padding="10")
        effect_frame.pack(fill=tk.X, pady=5)

        self.enable_effect = tk.BooleanVar(value=self.config.get("enable_effect", True))
        ttk.Checkbutton(effect_frame, text="添加视频特效（需要在坐标设置中配置特效按钮位置）",
                       variable=self.enable_effect).pack(side=tk.LEFT)

        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)

        self.start_btn = ttk.Button(btn_frame, text="开始自动化", command=self.start_automation, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_automation, width=10, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="打开剪映", command=self.open_jianying, width=10).pack(side=tk.LEFT, padx=10)

        # 进度和日志
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.status_var).pack(anchor=tk.W)

    def create_coord_page(self):
        main_frame = ttk.Frame(self.coord_page, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 实时坐标显示
        pos_frame = ttk.LabelFrame(main_frame, text="实时鼠标位置", padding="10")
        pos_frame.pack(fill=tk.X, pady=5)

        self.pos_label = ttk.Label(pos_frame, text="X: 0, Y: 0", font=("Consolas", 14))
        self.pos_label.pack()

        ttk.Label(pos_frame, text="提示：移动鼠标到目标位置，记下坐标后填入下方", foreground="gray").pack()

        # 坐标配置列表
        coord_list_frame = ttk.LabelFrame(main_frame, text="坐标配置（首次使用必须设置）", padding="10")
        coord_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 创建坐标输入框
        self.coord_vars = {}
        coords_info = [
            ("start_create", "开始制作按钮"),
            ("import_btn", "导入按钮"),
            ("add_to_track", "添加到轨道(+号)"),
            ("text_menu", "文本菜单"),
            ("smart_subtitle", "智能字幕"),
            ("start_recognize", "开始识别"),
            ("subtitle_select_all", "字幕全选(Ctrl+A后的位置)"),
            ("subtitle_style_btn", "字幕样式按钮"),
            ("font_family_input", "字体输入框"),
            ("font_size_input", "字号输入框"),
            ("font_color_btn", "字体颜色按钮"),
            ("color_gold", "金色选项"),
            ("audio_menu", "音频菜单"),
            ("audio_import", "音频导入按钮"),
            ("effect_menu", "特效菜单"),
            ("effect_select", "选择特效"),
            ("effect_apply", "应用特效"),
            ("export_btn", "导出按钮"),
            ("export_confirm", "确认导出"),
        ]

        for i, (name, desc) in enumerate(coords_info):
            row = ttk.Frame(coord_list_frame)
            row.pack(fill=tk.X, pady=2)

            ttk.Label(row, text=f"{desc}:", width=18).pack(side=tk.LEFT)
            ttk.Label(row, text="X:").pack(side=tk.LEFT)

            x_var = tk.StringVar(value=str(self.config["coords"].get(name, {}).get("x", 0)))
            y_var = tk.StringVar(value=str(self.config["coords"].get(name, {}).get("y", 0)))

            ttk.Entry(row, textvariable=x_var, width=6).pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text="Y:").pack(side=tk.LEFT)
            ttk.Entry(row, textvariable=y_var, width=6).pack(side=tk.LEFT, padx=2)

            self.coord_vars[name] = {"x": x_var, "y": y_var, "desc": desc}

        # 保存按钮
        ttk.Button(coord_list_frame, text="保存坐标配置", command=self.save_coords, width=15).pack(pady=10)

    def create_config_page(self):
        main_frame = ttk.Frame(self.config_page, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 路径配置
        paths = [
            ("jianying_path", "剪映程序路径"),
            ("video_source_path", "视频素材文件夹"),
            ("audio_source_path", "配音文件夹"),
            ("export_path", "导出文件夹"),
        ]

        self.path_vars = {}
        for name, desc in paths:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=f"{desc}:", width=15).pack(side=tk.LEFT)
            var = tk.StringVar(value=self.config.get(name, ""))
            self.path_vars[name] = var
            ttk.Entry(frame, textvariable=var, width=55).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame, text="选择", width=6,
                      command=lambda n=name: self.select_path(n)).pack(side=tk.LEFT)

        ttk.Button(main_frame, text="保存配置", command=self.save_path_config, width=15).pack(pady=20)

    def select_path(self, name):
        if name == "jianying_path":
            path = filedialog.askopenfilename(title="选择剪映程序", filetypes=[("可执行文件", "*.exe")])
        else:
            path = filedialog.askdirectory(title="选择文件夹")
        if path:
            self.path_vars[name].set(path)

    def save_path_config(self):
        for name, var in self.path_vars.items():
            self.config[name] = var.get()
        self.config["subtitle_style"] = {
            "font_family": self.subtitle_font.get(),
            "font_size": self.subtitle_size.get(),
            "color": self.subtitle_color.get(),
        }
        self.config["videos_per_folder"] = int(self.videos_per_folder.get())
        self.config["bgm_path"] = self.bgm_path.get()
        self.config["enable_bgm"] = self.enable_bgm.get()
        self.config["enable_effect"] = self.enable_effect.get()
        save_config(self.config)
        messagebox.showinfo("成功", "配置已保存")

    def save_coords(self):
        for name, vars in self.coord_vars.items():
            try:
                x = int(vars["x"].get())
                y = int(vars["y"].get())
                self.config["coords"][name] = {"x": x, "y": y, "desc": vars["desc"]}
            except ValueError:
                pass
        save_config(self.config)
        messagebox.showinfo("成功", "坐标配置已保存")

    def start_position_tracker(self):
        def update_pos():
            try:
                import pyautogui
                x, y = pyautogui.position()
                self.pos_label.config(text=f"X: {x}, Y: {y}")
            except:
                pass
            self.root.after(100, update_pos)
        update_pos()

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def select_audio(self):
        path = filedialog.askopenfilename(
            title="选择配音文件",
            initialdir=self.config["audio_source_path"],
            filetypes=[("音频文件", "*.mp3 *.wav *.m4a")]
        )
        if path:
            self.audio_path.set(path)

    def show_audio_list(self):
        audio_dir = self.config["audio_source_path"]
        if not os.path.exists(audio_dir):
            messagebox.showerror("错误", f"目录不存在: {audio_dir}")
            return

        files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
        if not files:
            messagebox.showinfo("提示", "没有找到音频文件")
            return

        # 创建选择窗口
        win = tk.Toplevel(self.root)
        win.title("选择音频文件")
        win.geometry("400x300")

        listbox = tk.Listbox(win, width=50, height=15)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for f in files:
            listbox.insert(tk.END, f)

        def on_select():
            sel = listbox.curselection()
            if sel:
                self.audio_path.set(os.path.join(audio_dir, files[sel[0]]))
                win.destroy()

        ttk.Button(win, text="选择", command=on_select).pack(pady=5)

    def select_video_folder(self):
        path = filedialog.askdirectory(title="选择视频素材文件夹")
        if path:
            self.video_source.set(path)

    def select_bgm_folder(self):
        path = filedialog.askdirectory(title="选择背景音乐文件夹")
        if path:
            self.bgm_path.set(path)

    def get_random_bgm(self):
        """随机选择一首背景音乐"""
        bgm_dir = self.bgm_path.get()
        if not bgm_dir or not os.path.exists(bgm_dir):
            return None
        bgm_files = [os.path.join(bgm_dir, f) for f in os.listdir(bgm_dir)
                    if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        if bgm_files:
            return random.choice(bgm_files)
        return None

    def open_jianying(self):
        path = self.config.get("jianying_path", "")
        if os.path.exists(path):
            import subprocess
            subprocess.Popen(path)
            self.log("已启动剪映")
        else:
            messagebox.showerror("错误", f"剪映路径不存在: {path}")

    def stop_automation(self):
        self.is_running = False
        self.log("用户停止了自动化")
        self.status_var.set("已停止")

    def start_automation(self):
        audio = self.audio_path.get()
        if not audio or not os.path.exists(audio):
            messagebox.showerror("错误", "请选择有效的配音文件")
            return

        # 检查坐标是否已设置
        coords = self.config.get("coords", {})
        missing = []
        for name, coord in coords.items():
            if coord.get("x", 0) == 0 and coord.get("y", 0) == 0:
                missing.append(coord.get("desc", name))

        if missing:
            messagebox.showwarning("警告", f"以下坐标未设置，请先在「坐标设置」页面配置：\n" + "\n".join(missing))
            return

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_running = True
        self.log_text.delete(1.0, tk.END)

        thread = threading.Thread(target=self.automation_task, args=(audio,))
        thread.daemon = True
        thread.start()

    def click_coord(self, name, wait=0.5):
        import pyautogui
        coord = self.config["coords"].get(name, {})
        x, y = coord.get("x", 0), coord.get("y", 0)
        desc = coord.get("desc", name)

        if x == 0 and y == 0:
            self.log(f"警告: {desc} 坐标未设置")
            return False

        self.log(f"点击 {desc} ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(wait)
        return True

    def automation_task(self, audio_path):
        import pyautogui
        import pygetwindow as gw

        try:
            self.log("=" * 40)
            self.log(f"开始处理: {os.path.basename(audio_path)}")
            self.log("=" * 40)

            # 1. 激活剪映窗口
            self.status_var.set("激活剪映窗口...")
            windows = gw.getWindowsWithTitle('剪映')
            if not windows:
                windows = gw.getWindowsWithTitle('JianyingPro')
            if windows:
                windows[0].activate()
                time.sleep(1)
            else:
                self.log("错误: 未找到剪映窗口，请先打开剪映")
                self.finish_task()
                return

            if not self.is_running:
                self.finish_task()
                return

            # 2. 点击开始制作
            self.status_var.set("创建新项目...")
            self.click_coord("start_create", wait=2)

            if not self.is_running:
                self.finish_task()
                return

            # 3. 导入音频 (Ctrl+I)
            self.status_var.set("导入音频...")
            self.log("导入音频文件...")
            pyautogui.hotkey('ctrl', 'i')
            time.sleep(1)

            # 输入文件路径
            import pyperclip
            pyperclip.copy(audio_path)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(2)

            self.log("音频导入完成")

            if not self.is_running:
                self.finish_task()
                return

            # 4. 收集并导入视频素材
            self.status_var.set("导入视频素材...")
            videos = self.collect_videos()
            for i, video in enumerate(videos):
                if not self.is_running:
                    break
                self.log(f"导入视频 {i+1}/{len(videos)}: {os.path.basename(video)}")
                pyautogui.hotkey('ctrl', 'i')
                time.sleep(0.5)
                pyperclip.copy(video)
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(1)

            if not self.is_running:
                self.finish_task()
                return

            # 5. 添加到轨道
            self.status_var.set("添加到轨道...")
            self.click_coord("add_to_track", wait=1)

            # 6. 生成字幕
            self.status_var.set("生成字幕...")
            self.click_coord("text_menu", wait=0.5)
            self.click_coord("smart_subtitle", wait=0.5)
            self.click_coord("start_recognize", wait=1)

            self.log("等待字幕识别完成...")
            time.sleep(30)  # 等待识别

            if not self.is_running:
                self.finish_task()
                return

            # 7. 调整字幕样式
            self.status_var.set("调整字幕样式...")
            self.log("调整字幕样式...")

            # 全选字幕 (Ctrl+A)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)

            # 点击字幕样式按钮
            self.click_coord("subtitle_style_btn", wait=0.5)

            # 修改字体
            selected_font_name = self.get_selected_font_search_name()
            self.click_coord("font_family_input", wait=0.3)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.typewrite(selected_font_name, interval=0.05)
            pyautogui.press('enter')
            time.sleep(0.5)

            # 修改字号
            self.click_coord("font_size_input", wait=0.3)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.typewrite(self.subtitle_size.get(), interval=0.05)
            time.sleep(0.3)

            # 修改颜色
            self.click_coord("font_color_btn", wait=0.5)
            self.click_coord("color_gold", wait=0.5)

            self.log(f"字幕样式: 字体{self.subtitle_font.get()}({selected_font_name}), 字号{self.subtitle_size.get()}, {self.subtitle_color.get()}")

            if not self.is_running:
                self.finish_task()
                return

            # 8. 添加特效
            if self.enable_effect.get():
                self.status_var.set("添加特效...")
                self.log("添加视频特效...")
                self.click_coord("effect_menu", wait=0.5)
                self.click_coord("effect_select", wait=0.5)
                self.click_coord("effect_apply", wait=1)
                self.log("特效添加完成")

            if not self.is_running:
                self.finish_task()
                return

            # 9. 添加背景音乐
            if self.enable_bgm.get():
                bgm_file = self.get_random_bgm()
                if bgm_file:
                    self.status_var.set("添加背景音乐...")
                    self.log(f"添加背景音乐: {os.path.basename(bgm_file)}")

                    # 点击音频菜单
                    self.click_coord("audio_menu", wait=0.5)
                    self.click_coord("audio_import", wait=0.5)

                    # 导入BGM文件
                    pyperclip.copy(bgm_file)
                    pyautogui.hotkey('ctrl', 'l')
                    time.sleep(0.3)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.3)
                    pyautogui.press('enter')
                    time.sleep(2)

                    self.log("背景音乐添加完成")
                else:
                    self.log("未找到BGM文件，跳过背景音乐")

            if not self.is_running:
                self.finish_task()
                return

            # 10. 导出
            self.status_var.set("导出视频...")
            self.click_coord("export_btn", wait=1)
            self.click_coord("export_confirm", wait=1)

            self.log("正在导出，请等待剪映完成...")
            self.log("=" * 40)
            self.log("自动化流程完成！")

            self.finish_task()

        except Exception as e:
            self.log(f"错误: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.finish_task()

    def collect_videos(self):
        video_dir = self.video_source.get()
        per_folder = int(self.videos_per_folder.get())
        collected = []

        if not os.path.exists(video_dir):
            self.log(f"视频目录不存在: {video_dir}")
            return collected

        subfolders = [os.path.join(video_dir, d) for d in os.listdir(video_dir)
                     if os.path.isdir(os.path.join(video_dir, d))]

        if not subfolders:
            subfolders = [video_dir]

        for folder in subfolders:
            videos = [os.path.join(folder, f) for f in os.listdir(folder)
                     if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
            if videos:
                selected = random.sample(videos, min(per_folder, len(videos)))
                collected.extend(selected)

        random.shuffle(collected)
        self.log(f"共收集 {len(collected)} 个视频素材")
        return collected

    def finish_task(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("完成")


def main():
    root = tk.Tk()
    app = JianyingAutoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
