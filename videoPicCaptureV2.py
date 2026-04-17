import os
import subprocess
from pathlib import Path

# ===================== 配置 =====================
VIDEO_FOLDER = "./videos"       # 视频放这里
OUTPUT_FOLDER = "./screenshots" # 截图输出到这里
SCENE_THRESHOLD = 20            # 场景灵敏度（越小切得越细）
# =================================================

# 自动创建文件夹
Path(VIDEO_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# 支持的视频格式
VIDEO_FORMATS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm")

def process_video(video_path):
    name = Path(video_path).stem  # 文件名（无后缀）
    output_pattern = os.path.join(OUTPUT_FOLDER, f"{name}_scene_%03d.jpg")

    # 【关键】修复版 FFmpeg 命令，无 batch_detect
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-filter:v", f"scdet=threshold={SCENE_THRESHOLD},thumbnail",
        "-q:v", "2",
        "-fps_mode", "vfr",
        "-y",
        output_pattern
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 处理成功：{name}")
    except Exception as e:
        print(f"❌ 处理失败：{name}")
        print("错误信息：", str(e))

# 批量扫描视频
def scan_videos():
    for file in os.listdir(VIDEO_FOLDER):
        path = os.path.join(VIDEO_FOLDER, file)
        if os.path.isfile(path) and file.lower().endswith(VIDEO_FORMATS):
            process_video(path)

if __name__ == "__main__":
    print("=== Windows 视频多场景最优截图工具 ===")
    scan_videos()
    print("\n🎉 全部处理完成！")