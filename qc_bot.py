import os
from moviepy.editor import VideoFileClip

def quality_control():
    print("[SYSTEM] QC Bot Initiated...")
    video_file = "final_tech_viral_video.mp4"
    
    if not os.path.exists(video_file):
        print("[-] QC FAIL: Video file missing!")
        exit(1)
        
    clip = VideoFileClip(video_file)
    duration = clip.duration
    size_mb = os.path.getsize(video_file) / (1024 * 1024)
    
    print(f"[INFO] Video Duration: {duration:.2f} seconds")
    print(f"[INFO] Video Size: {size_mb:.2f} MB")
    
    if duration > 60:
        print("[-] QC FAIL: Video length exceeds 60 seconds (Not a Short/Reel)!")
        exit(1)
        
    if size_mb < 0.5:
        print("[-] QC FAIL: Video file too small, possible render error!")
        exit(1)
        
    print("[+] QC PASS: Video is mathematically perfect and INSTA_READY! ✅")

if __name__ == "__main__":
    quality_control()
