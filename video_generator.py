# -*- coding: utf-8 -*-
"""
百家号引流视频生成器
功能：文案 → 图片 → 视频 → 配音 → 合成输出
"""

import os
import asyncio
import requests
import time
import json
import urllib3
from datetime import datetime
from PIL import Image
import edge_tts
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 导入配置
from config import (
    JIMENG_API_URL, JIMENG_API_KEY, JIMENG_MODEL, OUTPUT_DIR, TEMP_DIR,
    TTS_VOICE, TTS_RATE, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_RATIO, FPS
)


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "clips"), exist_ok=True)


# ==================== 即梦API图片生成 ====================

def generate_image_prompt(index, theme="宇宙仙侠"):
    """生成图片提示词 - 宇宙仙侠风格"""
    prompts = [
        "宇宙星空背景，一个孤独的身影站在悬崖边，仙侠风格，紫色星云，金色光芒，史诗感，电影级画质，8K超清",
        "浩瀚宇宙中漂浮的仙山，云雾缭绕，星河璀璨，一道人影负手而立，仙侠古风，神秘氛围，超高清画质",
        "星空下的古老宫殿，银河倒映，仙鹤飞舞，紫金色调，东方玄幻风格，大气磅礴，电影质感",
        "宇宙深处的修仙者，周身环绕星辰，长袍飘逸，背对观众望向星河，孤独而坚定，仙侠史诗风格，8K画质"
    ]
    return prompts[index % len(prompts)]


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
        print(f"  正在生成图片: {prompt[:30]}...")
        response = requests.post(JIMENG_API_URL, headers=headers, json=payload, timeout=180, verify=False)

        if response.status_code == 200:
            result = response.json()
            # 解析返回的图片URL
            if result.get("data") and len(result["data"]) > 0:
                image_url = result["data"][0].get("url")

                if image_url:
                    # 下载图片
                    img_response = requests.get(image_url, timeout=60, verify=False)
                    with open(save_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"  图片已保存: {save_path}")
                    return True

                # 如果是base64格式
                b64_data = result["data"][0].get("b64_json")
                if b64_data:
                    import base64
                    img_bytes = base64.b64decode(b64_data)
                    with open(save_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"  图片已保存: {save_path}")
                    return True

        print(f"  API返回: {response.status_code} - {response.text[:200]}")
        return False

    except Exception as e:
        print(f"  生成图片失败: {e}")
        return False


def generate_images(num_images=4):
    """生成多张图片"""
    print("\n" + "="*50)
    print("步骤1: 生成图片")
    print("="*50)

    image_paths = []
    for i in range(num_images):
        prompt = generate_image_prompt(i)
        save_path = os.path.join(TEMP_DIR, "images", f"image_{i+1}.png")

        if call_jimeng_api(prompt, save_path):
            image_paths.append(save_path)
        else:
            print(f"  警告: 第{i+1}张图片生成失败")

        # 避免API限流
        if i < num_images - 1:
            time.sleep(2)

    return image_paths


# ==================== 文字转语音 ====================

async def text_to_speech_async(text, output_path):
    """异步文字转语音"""
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
    await communicate.save(output_path)


def text_to_speech(text, output_path):
    """文字转语音 - 同步包装"""
    print("\n" + "="*50)
    print("步骤2: 生成语音")
    print("="*50)
    print(f"  使用声音: {TTS_VOICE}")
    print(f"  文案长度: {len(text)} 字")

    asyncio.run(text_to_speech_async(text, output_path))
    print(f"  语音已保存: {output_path}")
    return output_path


# ==================== 图片转视频 ====================

def create_image_clip(image_path, duration, effect="zoom_in"):
    """创建带动效的图片视频片段"""

    # 加载图片并调整尺寸
    img = Image.open(image_path)
    img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
    temp_img_path = image_path.replace(".png", "_resized.png")
    img.save(temp_img_path)

    clip = ImageClip(temp_img_path, duration=duration)

    # 添加缩放动效
    if effect == "zoom_in":
        # 缓慢放大效果
        clip = clip.resized(lambda t: 1 + 0.1 * t / duration)
    elif effect == "zoom_out":
        # 缓慢缩小效果
        clip = clip.resized(lambda t: 1.1 - 0.1 * t / duration)

    return clip


def images_to_video(image_paths, audio_path, output_path):
    """将图片合成为视频并添加音频"""
    print("\n" + "="*50)
    print("步骤3: 合成视频")
    print("="*50)

    # 获取音频时长
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    print(f"  音频时长: {total_duration:.1f} 秒")

    # 计算每张图片的时长
    num_images = len(image_paths)
    duration_per_image = total_duration / num_images
    print(f"  图片数量: {num_images}")
    print(f"  每张时长: {duration_per_image:.1f} 秒")

    # 创建视频片段
    clips = []
    effects = ["zoom_in", "zoom_out", "zoom_in", "zoom_out"]

    for i, img_path in enumerate(image_paths):
        print(f"  处理图片 {i+1}/{num_images}: {os.path.basename(img_path)}")
        effect = effects[i % len(effects)]
        clip = create_image_clip(img_path, duration_per_image, effect)
        clips.append(clip)

    # 拼接所有片段
    print("  拼接视频片段...")
    final_video = concatenate_videoclips(clips, method="compose")

    # 添加音频
    print("  添加音频...")
    final_video = final_video.with_audio(audio)

    # 输出视频
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
    audio.close()
    final_video.close()
    for clip in clips:
        clip.close()

    print(f"  视频生成完成!")
    return output_path


# ==================== 主流程 ====================

def generate_video_from_text(text, video_name=None):
    """从文案生成完整视频"""

    ensure_dirs()

    if video_name is None:
        video_name = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n" + "="*60)
    print(f"开始生成视频: {video_name}")
    print("="*60)

    # 步骤1: 生成图片
    image_paths = generate_images(4)
    if len(image_paths) < 2:
        print("错误: 图片生成失败，无法继续")
        return None

    # 步骤2: 生成语音
    audio_path = os.path.join(TEMP_DIR, "audio", f"{video_name}.mp3")
    text_to_speech(text, audio_path)

    # 步骤3: 合成视频
    output_path = os.path.join(OUTPUT_DIR, f"{video_name}.mp4")
    images_to_video(image_paths, audio_path, output_path)

    print("\n" + "="*60)
    print("视频生成完成!")
    print(f"输出路径: {output_path}")
    print("="*60)

    return output_path


# ==================== 测试 ====================

if __name__ == "__main__":
    # 测试文案
    test_text = """你是不是也有过这样的时刻：明明自己没做错什么，却被所有人否定？

那种感觉我太懂了。你站在人群中间，所有人都在朝一个方向走，只有你，倔强地站在原地。

这些年，你一个人扛过来的东西，没人知道。但你知道吗？你能走到今天，本身就是一种胜利。

愿你往后余生，走得坚定，活得从容。"""

    # 生成视频
    generate_video_from_text(test_text, "测试视频")
