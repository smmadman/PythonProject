import os
import subprocess
from pathlib import Path

# ===================== 配置 =====================
VIDEO_FOLDER = "./videos"
OUTPUT_FOLDER = "./screenshots"
CAPTURE_INTERVAL = 2   # 每 2 秒截一张（可改 1/3/10）
# =================================================

Path(VIDEO_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

VIDEO_FORMATS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm")

def process_video(video_path):
    name = Path(video_path).stem
    output_pattern = os.path.join(OUTPUT_FOLDER, f"{name}_shot_%03d.jpg")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{CAPTURE_INTERVAL}",  # 核心：按时间截图
        "-q:v", "2",
        "-y",
        output_pattern
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 处理成功：{name}")
    except Exception as e:
        print(f"❌ 处理失败：{name}")

def scan_videos():
    for file in os.listdir(VIDEO_FOLDER):
        path = os.path.join(VIDEO_FOLDER, file)
        if os.path.isfile(path) and file.lower().endswith(VIDEO_FORMATS):
            process_video(path)

if __name__ == "__main__":
    print("=== PPT/静态图视频 定时截图工具 ===")
    scan_videos()
    print("\n🎉 全部处理完成！")