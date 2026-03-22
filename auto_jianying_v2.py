# -*- coding: utf-8 -*-
"""
剪映自动化工具 - 图像识别版本
使用截图匹配来定位按钮，不依赖固定坐标
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
import time
import random
from datetime import datetime
import pyautogui
import pyperclip

# 配置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "jianying_config.json")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "jianying_images")

DEFAULT_CONFIG = {
    "jianying_path": r"D:\A压缩文件\剪映5.9版本免激活\JianyingPro\JianyingPro.exe",
    "video_source_path": r"D:\BaiduNetdiskDownload\自然风景视频素材",
    "audio_source_path": r"D:\A百家号带货视频\A带货配音",
    "export_path": r"D:\A百家号带货视频\A剪映视频",
    "bgm_path": r"D:\A百家号带货视频\BGM",
    "videos_per_folder": 3,
    "enable_bgm": True,
    "enable_effect": True,
    "confidence": 0.8,  # 图像匹配置信度
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

class ImageMatcher:
    """图像匹配工具类"""

    def __init__(self, images_dir, confidence=0.8):
        self.images_dir = images_dir
        self.confidence = confidence
        os.makedirs(images_dir, exist_ok=True)

    def get_image_path(self, name):
        """获取按钮截图路径"""
        return os.path.join(self.images_dir, f"{name}.png")

    def capture_button(self, name, region=None):
        """截取按钮图片并保存"""
        print(f"请将鼠标移动到【{name}】按钮上方")
        print("3秒后将截取鼠标周围50x50像素区域...")
        time.sleep(3)

        x, y = pyautogui.position()
        # 截取鼠标周围区域
        left = max(0, x - 25)
        top = max(0, y - 25)

        screenshot = pyautogui.screenshot(region=(left, top, 50, 50))
        img_path = self.get_image_path(name)
        screenshot.save(img_path)
        print(f"已保存: {img_path}")
        return img_path

    def find_button(self, name, timeout=10, click=False):
        """在屏幕上查找按钮"""
        img_path = self.get_image_path(name)
        if not os.path.exists(img_path):
            print(f"警告: 未找到按钮图片 {name}，请先截取")
            return None

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(img_path, confidence=self.confidence)
                if location:
                    center = pyautogui.center(location)
                    if click:
                        pyautogui.click(center)
                    return center
            except Exception as e:
                pass
            time.sleep(0.3)

        return None

    def click_button(self, name, timeout=10, wait_after=0.5):
        """查找并点击按钮"""
        pos = self.find_button(name, timeout=timeout, click=True)
        if pos:
            time.sleep(wait_after)
            return True
        return False

    def wait_for_button(self, name, timeout=60):
        """等待按钮出现"""
        return self.find_button(name, timeout=timeout) is not None

class JianyingAutoGUI:
    """剪映自动化GUI - 图像识别版"""

    def __init__(self, root):
        self.root = root
        self.root.title("剪映自动化工具 (图像识别版)")
        self.root.geometry("950x750")
        self.config = load_config()
        self.is_running = False
        self.matcher = ImageMatcher(IMAGES_DIR, self.config.get("confidence", 0.8))

        # 需要截取的按钮列表
        self.buttons_to_capture = [
            ("start_create", "开始制作"),
            ("import_first", "导入按钮(第一次)"),
            ("import_after", "导入按钮(后续)"),
            ("import_local", "本地"),
            ("add_to_track", "添加到轨道+号"),
            ("text_menu", "文字/文本"),
            ("smart_subtitle", "智能字幕"),
            ("recognize_btn", "开始识别"),
            ("audio_menu", "音频"),
            ("effect_menu", "特效"),
            ("export_btn", "导出"),
            ("export_confirm", "确认导出"),
        ]

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 标签页1：视频制作
        main_page = ttk.Frame(notebook)
        notebook.add(main_page, text="  视频制作  ")
        self.create_main_page(main_page)

        # 标签页2：按钮截图
        capture_page = ttk.Frame(notebook)
        notebook.add(capture_page, text="  按钮截图(首次必做)  ")
        self.create_capture_page(capture_page)

        # 标签页3：路径配置
        config_page = ttk.Frame(notebook)
        notebook.add(config_page, text="  路径配置  ")
        self.create_config_page(config_page)

    def create_main_page(self, parent):
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 音频选择
        audio_frame = ttk.LabelFrame(main_frame, text="1. 选择配音文件", padding="10")
        audio_frame.pack(fill=tk.X, pady=5)

        self.audio_path = tk.StringVar()
        ttk.Entry(audio_frame, textvariable=self.audio_path, width=55).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(audio_frame, text="选择", command=self.select_audio, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(audio_frame, text="列表", command=self.show_audio_list, width=8).pack(side=tk.LEFT)

        # 2. 视频素材
        video_frame = ttk.LabelFrame(main_frame, text="2. 视频素材", padding="10")
        video_frame.pack(fill=tk.X, pady=5)

        row1 = ttk.Frame(video_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="素材文件夹:").pack(side=tk.LEFT)
        self.video_source = tk.StringVar(value=self.config["video_source_path"])
        ttk.Entry(row1, textvariable=self.video_source, width=45).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1, text="选择", command=self.select_video_folder, width=6).pack(side=tk.LEFT)

        row2 = ttk.Frame(video_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="每文件夹取:").pack(side=tk.LEFT)
        self.videos_per_folder = tk.StringVar(value=str(self.config["videos_per_folder"]))
        ttk.Combobox(row2, textvariable=self.videos_per_folder, width=5,
                    values=["1","2","3","4","5"]).pack(side=tk.LEFT, padx=5)
        ttk.Label(row2, text="个视频").pack(side=tk.LEFT)

        # 3. 背景音乐
        bgm_frame = ttk.LabelFrame(main_frame, text="3. 背景音乐", padding="10")
        bgm_frame.pack(fill=tk.X, pady=5)

        self.enable_bgm = tk.BooleanVar(value=self.config.get("enable_bgm", True))
        ttk.Checkbutton(bgm_frame, text="添加背景音乐", variable=self.enable_bgm).pack(side=tk.LEFT)

        ttk.Label(bgm_frame, text="  BGM文件夹:").pack(side=tk.LEFT)
        self.bgm_path = tk.StringVar(value=self.config.get("bgm_path", ""))
        ttk.Entry(bgm_frame, textvariable=self.bgm_path, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(bgm_frame, text="选择", command=self.select_bgm_folder, width=6).pack(side=tk.LEFT)

        # 4. 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="开始自动化", command=self.start_automation, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_automation, width=10, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="打开剪映", command=self.open_jianying, width=10).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="测试识别", command=self.test_recognition, width=10).pack(side=tk.LEFT, padx=10)

        # 5. 日志
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="就绪 - 首次使用请先到「按钮截图」页面截取按钮图片")
        ttk.Label(main_frame, textvariable=self.status_var, foreground="blue").pack(anchor=tk.W)

    def create_capture_page(self, parent):
        """创建按钮截图页面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 说明
        info_frame = ttk.LabelFrame(main_frame, text="使用说明", padding="10")
        info_frame.pack(fill=tk.X, pady=5)

        info_text = """图像识别需要先截取剪映各个按钮的图片作为模板。
操作步骤：
1. 先打开剪映
2. 点击下方按钮旁边的「截取」
3. 在3秒内将鼠标移动到剪映对应按钮上
4. 程序会自动截取鼠标周围区域并保存

提示：截取时确保按钮完整显示，不要有遮挡"""
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

        # 按钮列表
        buttons_frame = ttk.LabelFrame(main_frame, text="按钮截图状态", padding="10")
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 创建滚动区域
        canvas = tk.Canvas(buttons_frame)
        scrollbar = ttk.Scrollbar(buttons_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_labels = {}
        for name, desc in self.buttons_to_capture:
            row = ttk.Frame(scrollable)
            row.pack(fill=tk.X, pady=3)

            ttk.Label(row, text=f"{desc}:", width=18).pack(side=tk.LEFT)

            # 状态标签
            img_path = self.matcher.get_image_path(name)
            if os.path.exists(img_path):
                status = "✓ 已截取"
                color = "green"
            else:
                status = "✗ 未截取"
                color = "red"

            status_label = ttk.Label(row, text=status, foreground=color, width=12)
            status_label.pack(side=tk.LEFT, padx=5)
            self.status_labels[name] = status_label

            ttk.Button(row, text="截取", width=8,
                      command=lambda n=name, d=desc: self.capture_button(n, d)).pack(side=tk.LEFT, padx=5)
            ttk.Button(row, text="测试", width=8,
                      command=lambda n=name, d=desc: self.test_button(n, d)).pack(side=tk.LEFT)

        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)

        ttk.Button(bottom_frame, text="打开截图文件夹", command=self.open_images_folder, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="刷新状态", command=self.refresh_capture_status, width=12).pack(side=tk.LEFT, padx=5)

    def create_config_page(self, parent):
        """创建配置页面"""
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        paths = [
            ("jianying_path", "剪映程序路径", "file"),
            ("video_source_path", "视频素材文件夹", "dir"),
            ("audio_source_path", "配音文件夹", "dir"),
            ("export_path", "导出文件夹", "dir"),
            ("bgm_path", "BGM文件夹", "dir"),
        ]

        self.path_vars = {}
        for name, desc, ptype in paths:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=f"{desc}:", width=15).pack(side=tk.LEFT)
            var = tk.StringVar(value=self.config.get(name, ""))
            self.path_vars[name] = var
            ttk.Entry(frame, textvariable=var, width=50).pack(side=tk.LEFT, padx=5)
            if ptype == "file":
                ttk.Button(frame, text="选择", width=6,
                          command=lambda v=var: v.set(filedialog.askopenfilename() or v.get())).pack(side=tk.LEFT)
            else:
                ttk.Button(frame, text="选择", width=6,
                          command=lambda v=var: v.set(filedialog.askdirectory() or v.get())).pack(side=tk.LEFT)

        # 识别置信度
        conf_frame = ttk.Frame(main_frame)
        conf_frame.pack(fill=tk.X, pady=10)
        ttk.Label(conf_frame, text="图像匹配置信度:").pack(side=tk.LEFT)
        self.confidence_var = tk.StringVar(value=str(self.config.get("confidence", 0.8)))
        ttk.Combobox(conf_frame, textvariable=self.confidence_var, width=8,
                    values=["0.6", "0.7", "0.8", "0.9"]).pack(side=tk.LEFT, padx=5)
        ttk.Label(conf_frame, text="(越低越容易匹配，但可能误识别)", foreground="gray").pack(side=tk.LEFT)

        ttk.Button(main_frame, text="保存配置", command=self.save_all_config, width=15).pack(pady=20)

    def save_all_config(self):
        for name, var in self.path_vars.items():
            self.config[name] = var.get()
        self.config["confidence"] = float(self.confidence_var.get())
        save_config(self.config)
        self.matcher.confidence = self.config["confidence"]
        messagebox.showinfo("成功", "配置已保存")

    def capture_button(self, name, desc):
        """截取按钮图片"""
        messagebox.showinfo("提示", f"点击确定后，请在3秒内将鼠标移动到剪映的【{desc}】按钮上")
        self.root.after(100, lambda: self._do_capture(name, desc))

    def _do_capture(self, name, desc):
        try:
            time.sleep(3)
            x, y = pyautogui.position()
            # 根据按钮类型调整截图大小
            if "add_to_track" in name or "+" in desc:
                # +号按钮截小一点，更精确
                left = max(0, x - 15)
                top = max(0, y - 15)
                width, height = 30, 30
            else:
                # 普通按钮
                left = max(0, x - 30)
                top = max(0, y - 12)
                width, height = 60, 24

            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            img_path = self.matcher.get_image_path(name)
            screenshot.save(img_path)
            self.log(f"已截取【{desc}】: {img_path}")
            self.refresh_capture_status()
            messagebox.showinfo("成功", f"已截取【{desc}】按钮图片\n尺寸: {width}x{height}")
        except Exception as e:
            messagebox.showerror("错误", f"截取失败: {e}")

    def test_button(self, name, desc):
        """测试按钮识别"""
        self.log(f"测试识别【{desc}】...")
        pos = self.matcher.find_button(name, timeout=3)
        if pos:
            self.log(f"✓ 找到【{desc}】位置: ({pos.x}, {pos.y})")
            pyautogui.moveTo(pos.x, pos.y)
            messagebox.showinfo("成功", f"找到【{desc}】，鼠标已移动到该位置")
        else:
            self.log(f"✗ 未找到【{desc}】")
            messagebox.showwarning("未找到", f"未能识别【{desc}】按钮，请确保剪映界面可见且按钮显示")

    def refresh_capture_status(self):
        """刷新截图状态"""
        for name, label in self.status_labels.items():
            img_path = self.matcher.get_image_path(name)
            if os.path.exists(img_path):
                label.config(text="✓ 已截取", foreground="green")
            else:
                label.config(text="✗ 未截取", foreground="red")

    def open_images_folder(self):
        os.makedirs(IMAGES_DIR, exist_ok=True)
        os.startfile(IMAGES_DIR)

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def select_audio(self):
        path = filedialog.askopenfilename(
            title="选择配音文件",
            initialdir=self.config.get("audio_source_path", ""),
            filetypes=[("音频文件", "*.mp3 *.wav *.m4a")]
        )
        if path:
            self.audio_path.set(path)

    def show_audio_list(self):
        audio_dir = self.config.get("audio_source_path", "")
        if not os.path.exists(audio_dir):
            messagebox.showerror("错误", f"目录不存在: {audio_dir}")
            return
        files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
        if not files:
            messagebox.showinfo("提示", "没有找到音频文件")
            return

        win = tk.Toplevel(self.root)
        win.title("选择音频")
        win.geometry("450x350")

        listbox = tk.Listbox(win, width=55, height=15)
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
        path = filedialog.askdirectory(title="选择BGM文件夹")
        if path:
            self.bgm_path.set(path)

    def get_random_bgm(self):
        bgm_dir = self.bgm_path.get()
        if not bgm_dir or not os.path.exists(bgm_dir):
            return None
        files = [os.path.join(bgm_dir, f) for f in os.listdir(bgm_dir)
                if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
        return random.choice(files) if files else None

    def open_jianying(self):
        path = self.config.get("jianying_path", "")
        if os.path.exists(path):
            import subprocess
            subprocess.Popen(path)
            self.log("已启动剪映")
        else:
            messagebox.showerror("错误", f"剪映路径不存在: {path}")

    def test_recognition(self):
        """测试所有按钮识别"""
        self.log("开始测试按钮识别...")
        found = 0
        for name, desc in self.buttons_to_capture:
            img_path = self.matcher.get_image_path(name)
            if os.path.exists(img_path):
                pos = self.matcher.find_button(name, timeout=2)
                if pos:
                    self.log(f"  ✓ {desc}: ({pos.x}, {pos.y})")
                    found += 1
                else:
                    self.log(f"  ✗ {desc}: 未找到")
            else:
                self.log(f"  - {desc}: 未截图")
        self.log(f"识别完成: {found}/{len(self.buttons_to_capture)}")

    def stop_automation(self):
        self.is_running = False
        self.log("用户停止了自动化")
        self.status_var.set("已停止")

    def collect_videos_by_folder(self):
        """按文件夹收集视频素材，返回 {文件夹名: [视频列表]}"""
        video_dir = self.video_source.get()
        per_folder = int(self.videos_per_folder.get())
        result = {}

        if not os.path.exists(video_dir):
            return result

        subfolders = [os.path.join(video_dir, d) for d in os.listdir(video_dir)
                     if os.path.isdir(os.path.join(video_dir, d))]
        if not subfolders:
            subfolders = [video_dir]

        for folder in subfolders:
            videos = [os.path.join(folder, f) for f in os.listdir(folder)
                     if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
            if videos:
                selected = random.sample(videos, min(per_folder, len(videos)))
                folder_name = os.path.basename(folder)
                result[folder_name] = selected

        return result

    def click_import_button(self, is_first=False):
        """点击导入按钮（区分第一次和后续）"""
        if is_first:
            # 第一次导入
            if self.matcher.click_button("import_first", timeout=5, wait_after=0.5):
                self.log("  ✓ 点击【导入(第一次)】")
                return True
        else:
            # 后续导入
            if self.matcher.click_button("import_after", timeout=5, wait_after=0.5):
                self.log("  ✓ 点击【导入(后续)】")
                return True

        # 都找不到就用快捷键
        self.log("  使用快捷键 Ctrl+I")
        pyautogui.hotkey('ctrl', 'i')
        time.sleep(0.8)
        return True

    def start_automation(self):
        """开始自动化"""
        audio = self.audio_path.get()
        if not audio or not os.path.exists(audio):
            messagebox.showerror("错误", "请选择有效的配音文件")
            return

        # 检查必要的按钮截图是否存在
        required = ["start_create", "import_first", "import_after", "add_to_track", "text_menu",
                   "smart_subtitle", "recognize_btn", "export_btn"]
        missing = []
        for name in required:
            if not os.path.exists(self.matcher.get_image_path(name)):
                for n, d in self.buttons_to_capture:
                    if n == name:
                        missing.append(d)
                        break

        if missing:
            messagebox.showwarning("警告", f"以下按钮未截图，请先到「按钮截图」页面截取：\n" + "\n".join(missing))
            return

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_running = True
        self.log_text.delete(1.0, tk.END)

        thread = threading.Thread(target=self.automation_task, args=(audio,))
        thread.daemon = True
        thread.start()

    def click_button_safe(self, name, desc, timeout=10, wait=0.5):
        """安全点击按钮（带日志）"""
        self.log(f"查找【{desc}】...")
        if self.matcher.click_button(name, timeout=timeout, wait_after=wait):
            self.log(f"  ✓ 已点击【{desc}】")
            return True
        else:
            self.log(f"  ✗ 未找到【{desc}】")
            return False

    def automation_task(self, audio_path):
        """自动化主任务"""
        try:
            import pygetwindow as gw

            self.log("=" * 40)
            self.log(f"开始处理: {os.path.basename(audio_path)}")
            self.log("=" * 40)

            # 1. 激活剪映窗口
            self.status_var.set("激活剪映...")
            windows = gw.getWindowsWithTitle('剪映')
            if not windows:
                windows = gw.getWindowsWithTitle('JianyingPro')
            if windows:
                windows[0].activate()
                time.sleep(1)
            else:
                self.log("错误: 未找到剪映窗口")
                self.finish_task()
                return

            if not self.is_running:
                self.finish_task()
                return

            # 2. 点击开始制作
            self.status_var.set("创建新项目...")
            if not self.click_button_safe("start_create", "开始制作", timeout=5):
                self.log("尝试使用快捷键 Ctrl+N...")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(2)

            if not self.is_running:
                self.finish_task()
                return

            # 3. 导入音频
            self.status_var.set("导入音频...")
            self.log(f"导入音频: {os.path.basename(audio_path)}")

            # 第一次导入
            self.click_import_button(is_first=True)
            time.sleep(0.5)

            # 输入文件路径
            pyperclip.copy(audio_path)
            pyautogui.hotkey('ctrl', 'l')  # 选中地址栏
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(2)

            # 音频添加到轨道
            self.log("音频添加到轨道...")
            self.click_button_safe("add_to_track", "添加到轨道", timeout=5)
            time.sleep(1)

            if not self.is_running:
                self.finish_task()
                return

            # 4. 按文件夹导入视频素材，每批导入后立刻添加到轨道
            self.status_var.set("导入视频素材...")
            videos_by_folder = self.collect_videos_by_folder()
            total_folders = len(videos_by_folder)
            self.log(f"共 {total_folders} 个文件夹的素材")

            folder_idx = 0
            for folder_name, videos in videos_by_folder.items():
                if not self.is_running:
                    break

                folder_idx += 1
                self.log(f"\n--- 文件夹 [{folder_idx}/{total_folders}]: {folder_name} ---")

                # 导入这个文件夹的所有视频
                for i, video in enumerate(videos):
                    if not self.is_running:
                        break

                    self.log(f"导入 [{i+1}/{len(videos)}]: {os.path.basename(video)}")

                    # 后续导入用第二个按钮位置
                    self.click_import_button(is_first=False)
                    time.sleep(0.5)

                    pyperclip.copy(video)
                    pyautogui.hotkey('ctrl', 'l')
                    time.sleep(0.2)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.2)
                    pyautogui.press('enter')
                    time.sleep(1.5)

                # 这批素材导入完，立刻添加到轨道
                self.log(f"将 {folder_name} 的素材添加到轨道...")
                self.click_button_safe("add_to_track", "添加到轨道", timeout=5)
                time.sleep(1)

            if not self.is_running:
                self.finish_task()
                return

            # 6. 生成字幕
            self.status_var.set("生成字幕...")
            self.log("生成智能字幕...")

            # 点击文字/文本菜单
            if not self.click_button_safe("text_menu", "文字菜单", timeout=5):
                self.log("尝试查找文本相关按钮...")

            time.sleep(0.5)

            # 点击智能字幕
            self.click_button_safe("smart_subtitle", "智能字幕", timeout=5)
            time.sleep(0.5)

            # 点击开始识别
            self.click_button_safe("recognize_btn", "开始识别", timeout=5)

            # 等待字幕识别完成
            self.log("等待字幕识别...")
            time.sleep(30)  # 根据音频长度可能需要调整

            if not self.is_running:
                self.finish_task()
                return

            # 7. 添加背景音乐
            if self.enable_bgm.get():
                bgm = self.get_random_bgm()
                if bgm:
                    self.status_var.set("添加背景音乐...")
                    self.log(f"添加BGM: {os.path.basename(bgm)}")

                    pyautogui.hotkey('ctrl', 'i')
                    time.sleep(0.8)
                    pyperclip.copy(bgm)
                    pyautogui.hotkey('ctrl', 'l')
                    time.sleep(0.2)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.2)
                    pyautogui.press('enter')
                    time.sleep(2)

                    # 添加到轨道
                    self.click_button_safe("add_to_track", "添加到轨道", timeout=3)
                    time.sleep(1)
                else:
                    self.log("未找到BGM文件")

            if not self.is_running:
                self.finish_task()
                return

            # 8. 导出视频
            self.status_var.set("导出视频...")
            self.log("开始导出...")

            # 点击导出按钮
            if not self.click_button_safe("export_btn", "导出", timeout=5):
                pyautogui.hotkey('ctrl', 'e')
                time.sleep(1)

            time.sleep(1)

            # 点击确认导出
            self.click_button_safe("export_confirm", "确认导出", timeout=5)

            self.log("=" * 40)
            self.log("自动化流程完成！请等待剪映导出...")
            self.log("=" * 40)

            self.finish_task()

        except Exception as e:
            self.log(f"错误: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.finish_task()

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
