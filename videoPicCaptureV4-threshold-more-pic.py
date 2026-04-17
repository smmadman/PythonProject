import os
import subprocess
from pathlib import Path

# ===================== 【正常视频】最强场景截图 =====================
VIDEO_FOLDER = "./videos"
OUTPUT_FOLDER = "./screenshots"

# 场景灵敏度（0~1），越小越灵敏！！！
# 0.05 = 超灵敏（几乎不漏场景）
# 0.1 = 灵敏
# 0.3 = 默认
# 重点：越小越灵敏！
SCENE_THRESHOLD = "0.01"
# ==================================================================

Path(VIDEO_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
VIDEO_FORMATS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm")

def process_video(video_path):
    name = Path(video_path).stem
    output_pattern = os.path.join(OUTPUT_FOLDER, f"{name}_scene_%03d.jpg")

    # 🔥 【最强正确写法】纯场景检测 + 每个场景输出一张
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-filter:v", f"select='gt(scene,{SCENE_THRESHOLD})',showinfo",
        "-vsync", "drop",
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
    print("=== 【正常视频】高精度场景截图工具 ===")
    scan_videos()
    print("\n🎉 全部处理完成！")