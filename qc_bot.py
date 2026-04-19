import os
from moviepy.editor import VideoFileClip

def quality_control():
    print("[SYSTEM] QC Bot Initiated...")
    video_file = "final_tech_viral_video.mp4"
    
    if not os.path.exists(video_file):
        print("[-] QC FAIL: Video file missing!")
        exit(1)
        
    clip = VideoFileClip(video_file)
    if clip.duration > 60 or (os.path.getsize(video_file) / 1048576) < 0.5:
        print("[-] QC FAIL: Metrics not met for Insta Reel.")
        exit(1)
        
    print("[+] QC PASS: Video is mathematically perfect and INSTA_READY! ✅")

if __name__ == "__main__":
    quality_control()
