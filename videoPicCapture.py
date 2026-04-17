import os
import re
import ffmpeg
from pathlib import Path

# ===================== 可配置项 =====================
VIDEO_FOLDER = "./videos"       # 你的视频文件夹
OUTPUT_FOLDER = "./screenshots" # 截图保存目录
SCENE_SENSITIVITY = 20           # 场景敏感度（0-100，越小切分越细）
QUALITY = 2                     # 截图质量 1-31（越小越清晰）
# ====================================================

# 自动创建目录
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# 支持的视频格式
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm"}

def extract_best_frames(video_path: str, output_dir: str):
    """
    自动检测场景 + 每个场景提取最优清晰度帧
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_pattern = os.path.join(output_dir, f"{video_name}_scene_%03d.jpg")

    try:
        print(f"正在处理：{video_path}")

        # FFmpeg 核心滤镜：场景检测 + 智能最优帧
        (
            ffmpeg
            .input(video_path)
            .filter(
                "scdet",
                threshold=SCENE_SENSITIVITY
            )
            .filter(
                "thumbnail",
                batch_detect=1
            )
            .output(
                output_pattern,
                qscale=QUALITY,
                fps_mode="vfr"
            )
            .overwrite_output()
            .run(quiet=True)
        )

        print(f"✅ 处理完成：{video_path}")

    except ffmpeg.Error as e:
        print(f"❌ 处理失败：{video_path}")
        print(f"错误信息：{e.stderr.decode()}")

def batch_process_videos(root_dir: str):
    """
    批量遍历目录所有视频
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in VIDEO_EXTS:
                video_path = os.path.join(root, file)
                extract_best_frames(video_path, OUTPUT_FOLDER)

if __name__ == "__main__":
    print("=" * 50)
    print(" 视频多场景最优截图工具 | Python 3.12.9")
    print("=" * 50)

    if not os.path.exists(VIDEO_FOLDER):
        print(f"创建视频目录：{VIDEO_FOLDER}")
        os.makedirs(VIDEO_FOLDER)
        print(f"请把视频放入 {VIDEO_FOLDER} 文件夹后重新运行！")
    else:
        batch_process_videos(VIDEO_FOLDER)

    print("\n🎉 全部任务完成！")