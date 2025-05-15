import os
import random
from moviepy.editor import VideoFileClip

def get_background_clip(folder_path="bg_vids", target_resolution=(720, 1280)):
    """Randomly select a background video, loop it if needed, and crop to fit TikTok format."""
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Background folder '{folder_path}' not found.")

    videos = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp4", ".mov"))]
    if not videos:
        raise FileNotFoundError(f"No background videos found in '{folder_path}'.")

    selected_path = os.path.join(folder_path, random.choice(videos))
    clip = VideoFileClip(selected_path)

    # Resize and center crop for 720x1280 TikTok style
    clip = clip.resize(height=1280)
    if clip.w < 720:
        clip = clip.resize(width=720)

    x_center = clip.w // 2
    clip = clip.crop(x_center - 360, x_center + 360, 0, 1280)

    return clip
