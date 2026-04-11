import os
from brain import get_script
from voice_engine import make_audio
from visual_engine import make_video

# GitHub Secrets se Keys uthana
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY", "").strip()
FAL_KEY = os.environ.get("FAL_KEY", "").strip()

def start_factory():
    print("🚀 AI Video Factory starting...")
    
    # Topic decide karna
    topic = "Pet ka acid aur samosa ki funny ladai"

    # 1. Brain: Scripting
    hindi_text, video_prompt = get_script(topic, NVIDIA_KEY)
    if not hindi_text: return

    # 2. Voice: Audio
    audio_file = make_audio(hindi_text)

    # 3. Visuals: Video
    video_file = make_video(video_prompt)
    if not video_file: return

    # 4. Merging with FFmpeg
    print("🎬 Final Editing (Merging)...")
    os.system(f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4")
    print("🔥 Factory Success! final_video.mp4 is ready.")

if __name__ == "__main__":
    start_factory()

