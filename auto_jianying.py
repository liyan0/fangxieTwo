# -*- coding: utf-8 -*-
"""
剪映自动化模块 - 使用 pyautogui 自动操作剪映
功能：导入音频、随机选择视频素材、匹配长度、生成字幕、导出视频
"""

import time
import os
import random
import pyautogui
import pyperclip
import subprocess
import json
from datetime import datetime

# 安全设置
pyautogui.FAILSAFE = True  # 鼠标移到左上角可以中断
pyautogui.PAUSE = 0.3

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "jianying_config.json")

# 默认配置
DEFAULT_CONFIG = {
    "jianying_path": r"D:\A压缩文件\剪映5.9版本免激活\JianyingPro\JianyingPro.exe",
    "video_source_path": r"D:\BaiduNetdiskDownload\自然风景视频素材",
    "audio_source_path": r"D:\A百家号带货视频\A带货配音",
    "export_path": r"D:\A百家号带货视频\A剪映视频",
    "videos_per_folder": 3,
    # 坐标配置（需要根据你的屏幕测量）
    "coords": {
        "start_create": {"x": 0, "y": 0, "desc": "开始制作按钮"},
        "import_btn": {"x": 0, "y": 0, "desc": "导入按钮"},
        "import_local": {"x": 0, "y": 0, "desc": "本地导入"},
        "file_path_input": {"x": 0, "y": 0, "desc": "文件路径输入框"},
        "open_btn": {"x": 0, "y": 0, "desc": "打开按钮"},
        "add_to_track": {"x": 0, "y": 0, "desc": "添加到轨道"},
        "audio_track": {"x": 0, "y": 0, "desc": "音频轨道位置"},
        "video_track": {"x": 0, "y": 0, "desc": "视频轨道位置"},
        "text_menu": {"x": 0, "y": 0, "desc": "文本菜单"},
        "smart_subtitle": {"x": 0, "y": 0, "desc": "智能字幕"},
        "start_recognize": {"x": 0, "y": 0, "desc": "开始识别"},
        "export_btn": {"x": 0, "y": 0, "desc": "导出按钮"},
        "export_confirm": {"x": 0, "y": 0, "desc": "确认导出"},
    }
}

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 补充缺失的配置项
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

class CoordinateMeasurer:
    """坐标测量工具"""

    def __init__(self):
        self.config = load_config()

    def measure_single(self, name, desc):
        """测量单个坐标"""
        print(f"\n请将鼠标移动到【{desc}】的位置")
        print("3秒后自动记录坐标...")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)

        x, y = pyautogui.position()
        print(f"已记录: {desc} = ({x}, {y})")

        self.config["coords"][name] = {"x": x, "y": y, "desc": desc}
        save_config(self.config)
        return x, y

    def measure_all(self):
        """测量所有需要的坐标"""
        print("=" * 50)
        print("剪映坐标测量工具")
        print("=" * 50)
        print("\n请先打开剪映，然后按照提示移动鼠标到对应位置")
        print("每个位置有3秒时间准备\n")

        coords_to_measure = [
            ("start_create", "开始制作按钮"),
            ("import_btn", "导入按钮"),
            ("import_local", "本地导入选项"),
            ("add_to_track", "添加到轨道按钮（素材上的+号）"),
            ("audio_track", "音频轨道位置"),
            ("video_track", "视频轨道位置"),
            ("text_menu", "文本菜单"),
            ("smart_subtitle", "智能字幕选项"),
            ("start_recognize", "开始识别按钮"),
            ("export_btn", "导出按钮"),
            ("export_confirm", "确认导出按钮"),
        ]

        input("按回车键开始测量...")

        for name, desc in coords_to_measure:
            self.measure_single(name, desc)
            input(f"\n按回车继续下一个...")

        print("\n" + "=" * 50)
        print("所有坐标已保存到 jianying_config.json")
        print("=" * 50)

    def show_current_position(self):
        """实时显示鼠标位置"""
        print("实时显示鼠标位置（按 Ctrl+C 退出）")
        print("-" * 30)
        try:
            while True:
                x, y = pyautogui.position()
                print(f"\r当前位置: X={x}, Y={y}    ", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n已退出")


class AutoJianying:
    """剪映自动化类"""

    def __init__(self):
        self.config = load_config()
        self.jianying_path = self.config["jianying_path"]
        self.video_source_path = self.config["video_source_path"]
        self.audio_source_path = self.config["audio_source_path"]
        self.export_path = self.config["export_path"]
        self.videos_per_folder = self.config["videos_per_folder"]
        self.coords = self.config["coords"]

    def log(self, msg):
        """打印日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")

    def click(self, coord_name, wait=0.5):
        """点击指定坐标"""
        coord = self.coords.get(coord_name, {})
        x = coord.get("x", 0)
        y = coord.get("y", 0)
        desc = coord.get("desc", coord_name)

        if x == 0 and y == 0:
            self.log(f"警告: {desc} 坐标未设置，请先运行坐标测量")
            return False

        self.log(f"点击 {desc} ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(wait)
        return True

    def start_jianying(self):
        """启动剪映"""
        if not os.path.exists(self.jianying_path):
            self.log(f"错误: 剪映路径不存在: {self.jianying_path}")
            return False

        self.log("启动剪映...")
        subprocess.Popen(self.jianying_path)
        time.sleep(5)  # 等待剪映启动
        return True

    def activate_jianying(self):
        """激活剪映窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle('剪映')
            if not windows:
                windows = gw.getWindowsWithTitle('JianyingPro')
            if windows:
                windows[0].activate()
                time.sleep(0.5)
                return True
            self.log("未找到剪映窗口")
            return False
        except Exception as e:
            self.log(f"激活窗口失败: {e}")
            return False

    def create_new_project(self):
        """创建新项目"""
        self.log("创建新项目...")
        return self.click("start_create", wait=2)

    def import_file(self, file_path):
        """导入文件"""
        self.log(f"导入文件: {os.path.basename(file_path)}")

        # 点击导入
        if not self.click("import_btn", wait=0.5):
            return False

        # 使用快捷键 Ctrl+I 导入（更可靠）
        pyautogui.hotkey('ctrl', 'i')
        time.sleep(1)

        # 输入文件路径
        pyperclip.copy(file_path)
        pyautogui.hotkey('ctrl', 'l')  # 选中路径栏
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')  # 粘贴路径
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(1)

        return True

    def collect_random_videos(self):
        """从各个文件夹随机收集视频"""
        self.log("收集视频素材...")
        collected = []

        if not os.path.exists(self.video_source_path):
            self.log(f"错误: 视频素材路径不存在: {self.video_source_path}")
            return collected

        # 获取所有子文件夹
        subfolders = []
        for item in os.listdir(self.video_source_path):
            item_path = os.path.join(self.video_source_path, item)
            if os.path.isdir(item_path):
                subfolders.append(item_path)

        if not subfolders:
            subfolders = [self.video_source_path]

        self.log(f"找到 {len(subfolders)} 个素材文件夹")

        # 从每个文件夹随机选择视频
        for folder in subfolders:
            videos = []
            for f in os.listdir(folder):
                if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                    videos.append(os.path.join(folder, f))

            if videos:
                selected = random.sample(videos, min(self.videos_per_folder, len(videos)))
                collected.extend(selected)
                self.log(f"  从 {os.path.basename(folder)} 选择了 {len(selected)} 个视频")

        random.shuffle(collected)  # 打乱顺序
        self.log(f"共收集 {len(collected)} 个视频")
        return collected

    def add_to_timeline(self):
        """将素材添加到时间线"""
        self.log("添加到时间线...")
        return self.click("add_to_track", wait=1)

    def generate_subtitles(self):
        """生成字幕"""
        self.log("生成字幕...")

        # 点击文本菜单
        if not self.click("text_menu", wait=0.5):
            return False

        # 点击智能字幕
        if not self.click("smart_subtitle", wait=0.5):
            return False

        # 点击开始识别
        if not self.click("start_recognize", wait=1):
            return False

        # 等待识别完成（根据音频长度调整）
        self.log("等待字幕识别完成...")
        time.sleep(30)  # 默认等待30秒

        return True

    def export_video(self, output_name=None):
        """导出视频"""
        self.log("导出视频...")

        # 点击导出按钮
        if not self.click("export_btn", wait=1):
            return False

        # 如果需要修改输出路径/名称
        if output_name:
            # 这里可以添加修改输出名称的逻辑
            pass

        # 点击确认导出
        if not self.click("export_confirm", wait=1):
            return False

        self.log("正在导出，请等待...")
        return True

    def process_audio(self, audio_path):
        """处理单个音频文件的完整流程"""
        self.log("=" * 50)
        self.log(f"开始处理: {os.path.basename(audio_path)}")
        self.log("=" * 50)

        # 1. 激活剪映
        if not self.activate_jianying():
            self.log("请先打开剪映")
            return False

        # 2. 创建新项目
        if not self.create_new_project():
            return False

        # 3. 导入音频
        if not self.import_file(audio_path):
            return False

        # 4. 收集并导入视频
        videos = self.collect_random_videos()
        for video in videos:
            self.import_file(video)

        # 5. 添加到时间线
        self.add_to_timeline()

        # 6. 生成字幕
        self.generate_subtitles()

        # 7. 导出
        self.export_video()

        self.log("处理完成！")
        return True


def main_menu():
    """主菜单"""
    print("\n" + "=" * 50)
    print("剪映自动化工具")
    print("=" * 50)
    print("1. 测量坐标（首次使用必须先执行）")
    print("2. 实时显示鼠标位置")
    print("3. 处理单个音频")
    print("4. 批量处理音频")
    print("5. 查看当前配置")
    print("6. 修改配置")
    print("0. 退出")
    print("-" * 50)

    choice = input("请选择: ").strip()
    return choice


def main():
    """主函数"""
    while True:
        choice = main_menu()

        if choice == "1":
            measurer = CoordinateMeasurer()
            measurer.measure_all()

        elif choice == "2":
            measurer = CoordinateMeasurer()
            measurer.show_current_position()

        elif choice == "3":
            config = load_config()
            audio_path = input(f"请输入音频文件路径 (默认目录: {config['audio_source_path']}): ").strip()
            if not audio_path:
                # 列出音频目录中的文件
                audio_dir = config['audio_source_path']
                if os.path.exists(audio_dir):
                    files = [f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav', '.m4a'))]
                    if files:
                        print("\n可用的音频文件:")
                        for i, f in enumerate(files, 1):
                            print(f"  {i}. {f}")
                        idx = input("选择文件编号: ").strip()
                        if idx.isdigit() and 1 <= int(idx) <= len(files):
                            audio_path = os.path.join(audio_dir, files[int(idx)-1])

            if audio_path and os.path.exists(audio_path):
                auto = AutoJianying()
                print("\n3秒后开始，请确保剪映已打开...")
                time.sleep(3)
                auto.process_audio(audio_path)
            else:
                print("文件不存在")

        elif choice == "4":
            config = load_config()
            audio_dir = config['audio_source_path']
            if os.path.exists(audio_dir):
                files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir)
                        if f.endswith(('.mp3', '.wav', '.m4a'))]
                if files:
                    print(f"\n找到 {len(files)} 个音频文件")
                    confirm = input("确认批量处理? (y/n): ").strip().lower()
                    if confirm == 'y':
                        auto = AutoJianying()
                        print("\n3秒后开始...")
                        time.sleep(3)
                        for audio in files:
                            auto.process_audio(audio)
                            time.sleep(2)
                else:
                    print("没有找到音频文件")
            else:
                print(f"音频目录不存在: {audio_dir}")

        elif choice == "5":
            config = load_config()
            print("\n当前配置:")
            print(f"  剪映路径: {config['jianying_path']}")
            print(f"  视频素材: {config['video_source_path']}")
            print(f"  音频目录: {config['audio_source_path']}")
            print(f"  导出目录: {config['export_path']}")
            print(f"  每文件夹取: {config['videos_per_folder']} 个视频")
            print("\n坐标配置:")
            for name, coord in config['coords'].items():
                print(f"  {coord.get('desc', name)}: ({coord.get('x', 0)}, {coord.get('y', 0)})")

        elif choice == "6":
            config = load_config()
            print("\n修改配置:")
            print("1. 剪映路径")
            print("2. 视频素材路径")
            print("3. 音频目录")
            print("4. 导出目录")
            print("5. 每文件夹取视频数量")
            sub = input("选择要修改的项: ").strip()

            if sub == "1":
                new_val = input(f"新路径 (当前: {config['jianying_path']}): ").strip()
                if new_val:
                    config['jianying_path'] = new_val
            elif sub == "2":
                new_val = input(f"新路径 (当前: {config['video_source_path']}): ").strip()
                if new_val:
                    config['video_source_path'] = new_val
            elif sub == "3":
                new_val = input(f"新路径 (当前: {config['audio_source_path']}): ").strip()
                if new_val:
                    config['audio_source_path'] = new_val
            elif sub == "4":
                new_val = input(f"新路径 (当前: {config['export_path']}): ").strip()
                if new_val:
                    config['export_path'] = new_val
            elif sub == "5":
                new_val = input(f"数量 (当前: {config['videos_per_folder']}): ").strip()
                if new_val.isdigit():
                    config['videos_per_folder'] = int(new_val)

            save_config(config)
            print("配置已保存")

        elif choice == "0":
            print("再见！")
            break

        else:
            print("无效选择")


if __name__ == "__main__":
    main()
