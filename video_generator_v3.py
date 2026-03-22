# -*- coding: utf-8 -*-
"""
百家号引流视频生成器 v3
功能：即梦生成图片 → 图片转视频(动效) → 拼接 → 字幕 → 配音 → 封面
"""

import os
import asyncio
import requests
import time
import re
import urllib3
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
JIMENG_API_URL = "https://jimengly.zeabur.app/v1/images/generations"
JIMENG_API_KEY = "31f6ed72dd0f109538bea4323ba48a5f,e4377e9da2db16832ab65270fddccbd9,240ddc9646fbd088634ded292572ab67"
JIMENG_MODEL = "jimeng"

OUTPUT_DIR = "D:/A百家号带货视频/成品视频"
TEMP_DIR = "D:/A百家号带货视频/临时文件"

# 语音配置 - 沉稳男声
TTS_VOICE = "zh-CN-YunjianNeural"  # 云健，沉稳有力
TTS_RATE = "-10%"  # 语速稍慢

# 视频配置 - 16:9横屏
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_RATIO = "16:9"
FPS = 30

# 字体配置
FONT_COVER = "C:/Windows/Fonts/msyhbd.ttc"  # 封面用微软雅黑粗体
FONT_SUBTITLE = "C:/Windows/Fonts/simhei.ttf"  # 字幕用黑体
SUBTITLE_SIZE = 80  # 字幕大小（放大）
SUBTITLE_COLOR = 'yellow'  # 字幕颜色
SUBTITLE_OFFSET_SECONDS = 0.8  # Delay subtitles to match TTS leading silence
SUBTITLE_MIN_DURATION = 0.6
SUBTITLE_BOTTOM_MARGIN = 150

# Cover layout safety for 16:9.
COVER_MAX_WIDTH_RATIO = 0.86
COVER_MAX_HEIGHT_RATIO = 0.58
COVER_MAX_FONT_SIZE = 150
COVER_MIN_FONT_SIZE = 88
COVER_LINE_SPACING = 34

# 背景音乐配置
BGM_PATH = None  # 背景音乐路径，设置后自动添加
BGM_VOLUME = 0.15  # 背景音乐音量（0.15表示15%，突出人声）


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "audio"), exist_ok=True)


# ==================== 即梦API图片生成 ====================

def generate_image_prompts():
    """生成图片提示词 - 宇宙仙侠风格"""
    return [
        "宇宙星空背景，一个孤独的身影站在悬崖边，仙侠风格，紫色星云，金色光芒，史诗感，电影级画质",
        "浩瀚宇宙中漂浮的仙山，云雾缭绕，星河璀璨，一道人影负手而立，仙侠古风，神秘氛围",
        "星空下的古老宫殿，银河倒映，仙鹤飞舞，紫金色调，东方玄幻风格，大气磅礴",
        "宇宙深处的修仙者，周身环绕星辰，长袍飘逸，背对观众望向星河，孤独而坚定，仙侠史诗风格"
    ]


def call_jimeng_api(prompt, save_path):
    """调用即梦API生成图片"""
    headers = {
        "Authorization": f"Bearer {JIMENG_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": JIMENG_MODEL,
        "prompt": prompt,
        "n": 1,
        "ratio": VIDEO_RATIO
    }

    try:
        print(f"    生成: {prompt[:25]}...")
        response = requests.post(JIMENG_API_URL, headers=headers, json=payload, timeout=180, verify=False)

        if response.status_code == 200:
            result = response.json()
            if result.get("data") and len(result["data"]) > 0:
                image_url = result["data"][0].get("url")
                if image_url:
                    img_response = requests.get(image_url, timeout=60, verify=False)
                    with open(save_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"    已保存: {os.path.basename(save_path)}")
                    return True
        print(f"    失败: {response.text[:100]}")
        return False
    except Exception as e:
        print(f"    错误: {e}")
        return False


def generate_images(num_images=4):
    """生成多张图片"""
    print("\n【步骤1】生成图片...")
    image_paths = []
    prompts = generate_image_prompts()

    for i in range(num_images):
        prompt = prompts[i % len(prompts)]
        save_path = os.path.join(TEMP_DIR, "images", f"img_{i+1}.png")

        if call_jimeng_api(prompt, save_path):
            image_paths.append(save_path)
        time.sleep(2)  # 避免API限流

    print(f"  成功生成 {len(image_paths)} 张图片")
    return image_paths


# ==================== 文字转语音 ====================

async def text_to_speech_async(text, output_path):
    """异步文字转语音"""
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
    await communicate.save(output_path)


def text_to_speech(text, output_path):
    """文字转语音"""
    print("\n【步骤2】生成语音...")
    print(f"  声音: {TTS_VOICE}")
    print(f"  字数: {len(text)}")
    asyncio.run(text_to_speech_async(text, output_path))
    print(f"  已保存: {os.path.basename(output_path)}")
    return output_path


# ==================== 图片转视频(带动效) ====================

def create_image_clip_with_effect(image_path, duration, effect_type):
    """创建带动效的图片视频片段 - 增强版"""
    # 加载并调整图片尺寸（放大一些以便做动效）
    img = Image.open(image_path)
    # 放大20%以便有空间做平移和缩放
    enlarged_width = int(VIDEO_WIDTH * 1.3)
    enlarged_height = int(VIDEO_HEIGHT * 1.3)
    img = img.resize((enlarged_width, enlarged_height), Image.Resampling.LANCZOS)
    temp_path = image_path.replace(".png", "_enlarged.png")
    img.save(temp_path)

    clip = ImageClip(temp_path, duration=duration)

    # 多种动效组合
    if effect_type == "zoom_in_slow":
        # 缓慢放大 + 居中
        def resize_func(t):
            scale = 1.0 + 0.1 * t / duration
            return scale
        clip = clip.resized(resize_func)
        clip = clip.with_position(('center', 'center'))

    elif effect_type == "zoom_out_slow":
        # 缓慢缩小
        def resize_func(t):
            scale = 1.1 - 0.1 * t / duration
            return scale
        clip = clip.resized(resize_func)
        clip = clip.with_position(('center', 'center'))

    elif effect_type == "pan_left_zoom":
        # 向左平移 + 轻微放大
        def pos_func(t):
            x = int(50 - 150 * t / duration)
            return (x, 'center')
        def resize_func(t):
            return 1.0 + 0.05 * t / duration
        clip = clip.resized(resize_func)
        clip = clip.with_position(pos_func)

    elif effect_type == "pan_right_zoom":
        # 向右平移 + 轻微放大
        def pos_func(t):
            x = int(-100 + 150 * t / duration)
            return (x, 'center')
        def resize_func(t):
            return 1.0 + 0.05 * t / duration
        clip = clip.resized(resize_func)
        clip = clip.with_position(pos_func)

    elif effect_type == "pan_up":
        # 向上平移
        def pos_func(t):
            y = int(50 - 100 * t / duration)
            return ('center', y)
        clip = clip.with_position(pos_func)

    elif effect_type == "pan_down":
        # 向下平移
        def pos_func(t):
            y = int(-50 + 100 * t / duration)
            return ('center', y)
        clip = clip.with_position(pos_func)

    else:
        # 默认居中
        clip = clip.with_position(('center', 'center'))

    return clip


def images_to_video_clips(image_paths, total_duration):
    """将图片转换为视频片段"""
    print("\n【步骤3】图片转视频...")
    clips = []
    num_images = len(image_paths)
    duration_per_image = total_duration / num_images

    # 多种动效交替使用
    effects = ["zoom_in_slow", "pan_left_zoom", "zoom_out_slow", "pan_right_zoom"]

    for i, img_path in enumerate(image_paths):
        effect = effects[i % len(effects)]
        print(f"  处理图片 {i+1}/{num_images}: {effect}")
        clip = create_image_clip_with_effect(img_path, duration_per_image, effect)
        clips.append(clip)

    return clips


# ==================== 字幕生成 ====================

def split_text_to_sentences(text):
    """Split article text into subtitle sentences."""
    sentences = re.split(r'[???\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 2]
    return sentences


def _subtitle_weight(sentence):
    """Use non-punctuation char count as a rough speaking-time weight."""
    clean = re.sub(r'[\s???????,.!?:;??"\'??()??\[\]-]', '', sentence)
    return max(len(clean), 1)


def _subtitle_timing(sentences, total_duration):
    if not sentences or total_duration <= 0:
        return []

    offset = min(max(SUBTITLE_OFFSET_SECONDS, 0), max(total_duration - 0.2, 0))
    available = max(total_duration - offset, 0.2)
    weights = [_subtitle_weight(s) for s in sentences]
    total_weight = sum(weights) or len(sentences)
    raw = [available * w / total_weight for w in weights]

    durations = [max(d, SUBTITLE_MIN_DURATION) for d in raw]
    total_allocated = sum(durations)
    if total_allocated > available:
        scale = available / total_allocated
        durations = [max(d * scale, 0.2) for d in durations]

    timings = []
    cursor = offset
    for i, d in enumerate(durations):
        if i == len(durations) - 1:
            d = max(total_duration - cursor, 0.2)
        timings.append((cursor, d))
        cursor += d
    return timings


def create_subtitle_clips(sentences, total_duration):
    """Create subtitle clips with weighted timing and start offset."""
    print("\n???4?????...")
    clips = []
    if not sentences:
        return clips

    timings = _subtitle_timing(sentences, total_duration)

    for i, sentence in enumerate(sentences):
        start_time, duration = timings[i]
        try:
            txt_clip = TextClip(
                text=sentence,
                font_size=SUBTITLE_SIZE,
                color=SUBTITLE_COLOR,
                font=FONT_SUBTITLE,
                stroke_color='black',
                stroke_width=3,
                size=(VIDEO_WIDTH - 200, None),
                method='caption'
            )
            txt_clip = txt_clip.with_position(('center', VIDEO_HEIGHT - SUBTITLE_BOTTOM_MARGIN))
            txt_clip = txt_clip.with_start(start_time)
            txt_clip = txt_clip.with_duration(duration)
            clips.append(txt_clip)
        except Exception as e:
            print(f"  ?? {i+1} ??: {e}")

    print(f"  ?? {len(clips)} ???")
    return clips


def _split_cover_title_lines(title, target_len=6, max_lines=3):
    text = re.sub(r'\s+', '', title or '')
    if not text:
        return ["未命名标题"]

    # 1) 优先按标点切分
    parts = [p for p in re.split(r'[，,。！？!?、；;：:]+', text) if p]
    if not parts:
        parts = [text]

    # 2) 标点切出来的每段若超过 8 字，再按 8 字拆分
    lines = []
    for part in parts:
        if len(part) <= 8:
            lines.append(part)
            continue
        start = 0
        while start < len(part):
            lines.append(part[start:start + 8])
            start += 8

    # 3) 最多 max_lines 行，超出的并入最后一行
    if len(lines) > max_lines:
        merged = lines[:max_lines - 1]
        merged.append(''.join(lines[max_lines - 1:]))
        lines = merged

    return lines


def _fit_cover_font(draw, lines):
    max_width = int(VIDEO_WIDTH * COVER_MAX_WIDTH_RATIO)
    max_height = int(VIDEO_HEIGHT * COVER_MAX_HEIGHT_RATIO)

    for font_size in range(COVER_MAX_FONT_SIZE, COVER_MIN_FONT_SIZE - 1, -4):
        try:
            font = ImageFont.truetype(FONT_COVER, font_size)
        except Exception:
            font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", font_size)

        widths = []
        heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            widths.append(bbox[2] - bbox[0])
            heights.append(bbox[3] - bbox[1])

        total_height = sum(heights) + COVER_LINE_SPACING * (len(lines) - 1)
        if max(widths) <= max_width and total_height <= max_height:
            return font, widths, heights

    font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", COVER_MIN_FONT_SIZE)
    widths = []
    heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    return font, widths, heights


def create_cover(title, output_path):
    """Generate 16:9 cover and keep long titles visible."""
    print("\n???5?????...")
    import random

    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), (10, 10, 30))
    draw = ImageDraw.Draw(img)

    for y in range(VIDEO_HEIGHT):
        r = int(10 + 20 * y / VIDEO_HEIGHT)
        g = int(5 + 15 * y / VIDEO_HEIGHT)
        b = int(30 + 50 * y / VIDEO_HEIGHT)
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b))

    draw = ImageDraw.Draw(img)

    for _ in range(30):
        x = random.randint(0, VIDEO_WIDTH)
        y = random.randint(0, VIDEO_HEIGHT)
        size = random.randint(2, 5)
        brightness = random.randint(200, 255)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(brightness, brightness, brightness))

    for _ in range(100):
        x = random.randint(0, VIDEO_WIDTH)
        y = random.randint(0, VIDEO_HEIGHT)
        brightness = random.randint(150, 255)
        draw.point((x, y), fill=(brightness, brightness, brightness))

    for _ in range(15):
        x = random.randint(50, VIDEO_WIDTH - 50)
        y = random.randint(50, VIDEO_HEIGHT - 50)
        length = random.randint(10, 25)
        for i in range(-length, length + 1):
            alpha = int(255 * (1 - abs(i) / length))
            if 0 <= x + i < VIDEO_WIDTH:
                draw.point((x + i, y), fill=(alpha, alpha, alpha))
        for i in range(-length, length + 1):
            alpha = int(255 * (1 - abs(i) / length))
            if 0 <= y + i < VIDEO_HEIGHT:
                draw.point((x, y + i), fill=(alpha, alpha, alpha))

    lines = _split_cover_title_lines(title, target_len=6, max_lines=3)
    font, widths, heights = _fit_cover_font(draw, lines)

    text_color = (255, 50, 50)
    shadow_color = (100, 0, 0)

    total_height = sum(heights) + COVER_LINE_SPACING * (len(lines) - 1)
    y = (VIDEO_HEIGHT - total_height) // 2

    for line, width, height in zip(lines, widths, heights):
        x = (VIDEO_WIDTH - width) // 2
        draw.text((x + 5, y + 5), line, font=font, fill=shadow_color)
        draw.text((x, y), line, font=font, fill=text_color)
        y += height + COVER_LINE_SPACING

    img.save(output_path)
    print(f"  ???: {os.path.basename(output_path)}")
    return output_path


def compose_final_video(image_clips, subtitle_clips, audio_path, output_path, bgm_path=None):
    """合成最终视频"""
    print("\n【步骤6】合成视频...")

    # 拼接图片视频
    print("  拼接视频片段...")
    video = concatenate_videoclips(image_clips, method="compose")

    # 添加字幕
    print("  添加字幕...")
    if subtitle_clips:
        video = CompositeVideoClip([video] + subtitle_clips)

    # 加载配音
    print("  添加配音...")
    voice_audio = AudioFileClip(audio_path)

    # 添加背景音乐
    if bgm_path and os.path.exists(bgm_path):
        print(f"  添加背景音乐: {os.path.basename(bgm_path)}")
        from moviepy.audio.AudioClip import CompositeAudioClip
        bgm_audio = AudioFileClip(bgm_path)

        # 如果背景音乐比视频短，循环播放
        if bgm_audio.duration < voice_audio.duration:
            loops = int(voice_audio.duration / bgm_audio.duration) + 1
            from moviepy import concatenate_audioclips
            bgm_audio = concatenate_audioclips([bgm_audio] * loops)

        # 裁剪到视频长度
        bgm_audio = bgm_audio.subclipped(0, voice_audio.duration)

        # 降低背景音乐音量
        bgm_audio = bgm_audio.with_volume_scaled(BGM_VOLUME)

        # 合成音频
        final_audio = CompositeAudioClip([voice_audio, bgm_audio])
        video = video.with_audio(final_audio)
    else:
        video = video.with_audio(voice_audio)

    # 输出
    print(f"  输出: {os.path.basename(output_path)}")
    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )

    # 清理
    video.close()
    voice_audio.close()
    for clip in image_clips:
        clip.close()

    return output_path


# ==================== 主流程 ====================

def generate_video(text, title, video_name=None, bgm_path=None):
    """生成完整视频"""
    ensure_dirs()

    if video_name is None:
        video_name = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n" + "=" * 60)
    print(f"开始生成视频: {video_name}")
    print("=" * 60)

    # 步骤1: 生成图片
    image_paths = generate_images(4)
    if len(image_paths) < 2:
        print("错误: 图片生成失败")
        return None

    # 步骤2: 生成语音
    audio_path = os.path.join(TEMP_DIR, "audio", f"{video_name}.mp3")
    text_to_speech(text, audio_path)

    # 获取音频时长
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    audio.close()
    print(f"  音频时长: {total_duration:.1f}秒")

    # 步骤3: 图片转视频
    image_clips = images_to_video_clips(image_paths, total_duration)

    # 步骤4: 生成字幕
    sentences = split_text_to_sentences(text)
    subtitle_clips = create_subtitle_clips(sentences, total_duration)

    # 步骤5: 生成封面
    cover_path = os.path.join(OUTPUT_DIR, f"{video_name}_封面.jpg")
    create_cover(title, cover_path)

    # 步骤6: 合成视频（带背景音乐）
    output_path = os.path.join(OUTPUT_DIR, f"{video_name}.mp4")
    compose_final_video(image_clips, subtitle_clips, audio_path, output_path, bgm_path or BGM_PATH)

    print("\n" + "=" * 60)
    print("完成!")
    print(f"视频: {output_path}")
    print(f"封面: {cover_path}")
    print("=" * 60)

    return output_path


# ==================== 测试 ====================

if __name__ == "__main__":
    test_text = """你是不是也有过这样的时刻：明明自己没做错什么，却被所有人否定？

那种感觉我太懂了。你站在人群中间，所有人都在朝一个方向走，只有你，倔强地站在原地。

这些年，你一个人扛过来的东西，没人知道。

但你知道吗？你能走到今天，本身就是一种胜利。

王阳明说过：此心光明，亦复何言。

关于如何在质疑声中保持内心的笃定，我在主页置顶的那条内容里聊得更透。

愿你往后余生，走得坚定，活得从容。"""

    test_title = "从今往后再没人敢小看你"

    generate_video(test_text, test_title, "测试v3")
