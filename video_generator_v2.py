# -*- coding: utf-8 -*-
"""
百家号引流视频生成器 v2
功能：文案 + 剪映动态素材 + 字幕 + 配音 → 成品视频
"""

import os
import asyncio
import requests
import time
import json
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# 导入配置
from config import (
    OUTPUT_DIR, TEMP_DIR, TTS_VOICE, TTS_RATE, FPS
)

# 剪映素材目录
JIANYING_DIR = "D:/A百家号带货视频/剪映视频"


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "audio"), exist_ok=True)


def get_available_videos():
    """获取所有可用的剪映视频素材"""
    videos = {}
    if os.path.exists(JIANYING_DIR):
        for folder in os.listdir(JIANYING_DIR):
            folder_path = os.path.join(JIANYING_DIR, folder)
            if os.path.isdir(folder_path):
                video_file = os.path.join(folder_path, f"{folder}.mp4")
                cover_file = os.path.join(folder_path, f"{folder}-封面.jpg")
                if os.path.exists(video_file):
                    videos[folder] = {
                        "video": video_file,
                        "cover": cover_file if os.path.exists(cover_file) else None
                    }
    return videos


def match_video_for_content(content, available_videos):
    """根据文案内容匹配最合适的视频素材"""
    # 关键词匹配
    keywords_map = {
        "一个人扛": "一个人扛过来的苦，没人能体会",
        "扛过来": "一个人扛过来的苦，没人能体会",
        "没人能体会": "一个人扛过来的苦，没人能体会",
        "吃过的苦": "你吃过的苦，终将变成你的铠甲",
        "铠甲": "你吃过的苦，终将变成你的铠甲",
        "与众不同": "你的与众不同，正在悄悄改变你的人生",
        "改变你的人生": "你的与众不同，正在悄悄改变你的人生",
        "笑到最后": "你这种人，注定是笑到最后的",
        "小看你": "从今往后，再没人敢小看你了",
        "否定": "从今往后，再没人敢小看你了",
        "坚持": "你的坚持，正在被证明是对的",
        "想你": "有个人正在想你，你知道吗",
        "偷偷爱你": "有人在偷偷爱你，你发现了吗",
        "不说爱": "有些人不说爱，却爱得最深",
        "深爱": "有些人不说爱，却爱得最深",
        "真话": "停下来，你该听听真话了",
        "消息": "这个消息，我必须第一时间告诉你",
    }

    for keyword, video_name in keywords_map.items():
        if keyword in content and video_name in available_videos:
            return video_name, available_videos[video_name]

    # 默认返回第一个可用的
    if available_videos:
        first_key = list(available_videos.keys())[0]
        return first_key, available_videos[first_key]

    return None, None


# ==================== 文字转语音 ====================

async def text_to_speech_async(text, output_path):
    """异步文字转语音"""
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
    await communicate.save(output_path)


def text_to_speech(text, output_path):
    """文字转语音"""
    print(f"  使用声音: {TTS_VOICE}")
    print(f"  文案长度: {len(text)} 字")
    asyncio.run(text_to_speech_async(text, output_path))
    print(f"  语音已保存: {output_path}")
    return output_path


# ==================== 字幕生成 ====================

def split_text_to_sentences(text):
    """将文案分割成句子用于字幕"""
    # 按标点分割
    sentences = re.split(r'[。！？\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def create_subtitle_clips(sentences, total_duration, video_size):
    """创建字幕片段"""
    width, height = video_size
    clips = []

    # 计算每句话的时长
    duration_per_sentence = total_duration / len(sentences)

    # 尝试加载中文字体
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
    ]

    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break

    for i, sentence in enumerate(sentences):
        start_time = i * duration_per_sentence

        # 创建字幕文本
        try:
            txt_clip = TextClip(
                text=sentence,
                font_size=48,
                color='white',
                font=font_path,
                stroke_color='black',
                stroke_width=2,
                size=(width - 100, None),
                method='caption'
            )
        except Exception as e:
            print(f"  字幕创建失败: {e}")
            continue

        # 设置位置和时间
        txt_clip = txt_clip.with_position(('center', height - 200))
        txt_clip = txt_clip.with_start(start_time)
        txt_clip = txt_clip.with_duration(duration_per_sentence)

        clips.append(txt_clip)

    return clips


# ==================== 封面生成 ====================

def create_cover(title, output_path, size=(1920, 1080)):
    """生成视频封面"""
    width, height = size

    # 创建渐变背景
    img = Image.new('RGB', (width, height), (20, 20, 40))
    draw = ImageDraw.Draw(img)

    # 添加渐变效果
    for y in range(height):
        r = int(20 + (60 - 20) * y / height)
        g = int(20 + (30 - 20) * y / height)
        b = int(40 + (80 - 40) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 加载字体
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]

    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 80)
                break
            except:
                continue

    if font is None:
        font = ImageFont.load_default()

    # 绘制标题文字
    draw = ImageDraw.Draw(img)

    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # 绘制文字阴影
    draw.text((x + 3, y + 3), title, font=font, fill=(0, 0, 0))
    # 绘制文字
    draw.text((x, y), title, font=font, fill=(255, 215, 0))  # 金色

    img.save(output_path)
    print(f"  封面已保存: {output_path}")
    return output_path


# ==================== 视频合成 ====================

def compose_video(bg_video_path, audio_path, text, title, output_path):
    """合成最终视频：背景视频 + 配音 + 字幕"""
    print("\n  加载背景视频...")
    bg_video = VideoFileClip(bg_video_path)

    print("  加载音频...")
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    # 如果背景视频比音频短，循环播放
    if bg_video.duration < audio_duration:
        loops_needed = int(audio_duration / bg_video.duration) + 1
        bg_video = concatenate_videoclips([bg_video] * loops_needed)

    # 裁剪到音频长度
    bg_video = bg_video.subclipped(0, audio_duration)

    # 替换音频
    bg_video = bg_video.with_audio(audio)

    video_size = (bg_video.w, bg_video.h)

    # 创建字幕
    print("  生成字幕...")
    sentences = split_text_to_sentences(text)
    subtitle_clips = create_subtitle_clips(sentences, audio_duration, video_size)

    # 合成视频
    print("  合成视频...")
    if subtitle_clips:
        final_video = CompositeVideoClip([bg_video] + subtitle_clips)
    else:
        final_video = bg_video

    # 输出
    print(f"  输出视频: {output_path}")
    final_video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )

    # 清理
    bg_video.close()
    audio.close()
    final_video.close()

    return output_path


# ==================== 主流程 ====================

def generate_video_v2(text, title, video_name=None):
    """生成完整视频（使用剪映素材）"""

    ensure_dirs()

    if video_name is None:
        video_name = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n" + "="*60)
    print(f"开始生成视频: {video_name}")
    print("="*60)

    # 步骤1: 匹配视频素材
    print("\n【步骤1】匹配视频素材...")
    available_videos = get_available_videos()
    print(f"  可用素材: {len(available_videos)} 个")

    matched_name, matched_video = match_video_for_content(text, available_videos)
    if not matched_video:
        print("  错误: 没有找到匹配的视频素材")
        return None

    print(f"  匹配素材: {matched_name}")

    # 步骤2: 生成语音
    print("\n【步骤2】生成语音...")
    audio_path = os.path.join(TEMP_DIR, "audio", f"{video_name}.mp3")
    text_to_speech(text, audio_path)

    # 步骤3: 生成封面
    print("\n【步骤3】生成封面...")
    cover_path = os.path.join(OUTPUT_DIR, f"{video_name}_封面.jpg")
    create_cover(title, cover_path)

    # 步骤4: 合成视频
    print("\n【步骤4】合成视频...")
    output_path = os.path.join(OUTPUT_DIR, f"{video_name}.mp4")
    compose_video(matched_video["video"], audio_path, text, title, output_path)

    print("\n" + "="*60)
    print("视频生成完成!")
    print(f"视频: {output_path}")
    print(f"封面: {cover_path}")
    print("="*60)

    return output_path


# ==================== 测试 ====================

if __name__ == "__main__":
    test_text = """你是不是也有过这样的时刻：明明自己没做错什么，却被所有人否定？

那种感觉我太懂了。你站在人群中间，所有人都在朝一个方向走，只有你，倔强地站在原地。

这些年，你一个人扛过来的东西，没人知道。但你知道吗？你能走到今天，本身就是一种胜利。

愿你往后余生，走得坚定，活得从容。"""

    test_title = "从今往后，再没人敢小看你了"

    generate_video_v2(test_text, test_title, "测试视频v2")
