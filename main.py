import os
import requests
from gtts import gTTS

# Super Filter: Har tarah ke hidden space aur Enter (\n, \r) ko kaat dega
raw_key = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_KEY = raw_key.replace('\n', '').replace('\r', '').replace(' ', '').strip()

def generate_story_and_prompt():
    print("Step 1: Generating Story and Prompt via NVIDIA API...")
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are a creative director. Give me a 1-line funny Hindi dialogue for a 3D animated character, and a 1-line English prompt to generate that character's video."},
            {"role": "user", "content": "Create a funny scene about a lazy potato."}
        ],
        "max_tokens": 150
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
        print("Generated Output:\n", result)
        # Testing pipeline ke liye static data
        dialogue = "Yaar, mujhe ubalne se pehle thoda sone do!"
        video_prompt = "A 3D Pixar style cute potato sleeping on a sofa, cinematic lighting, highly detailed."
        return dialogue, video_prompt
    else:
        print("Error in API:", response.text)
        return None, None

def generate_audio(text):
    print("Step 2: Generating Audio (TTS)...")
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save("audio.mp3")
    print("Audio saved as audio.mp3")

def generate_video(prompt):
    print("Step 3: Generating Video...")
    os.system("ffmpeg -y -f lavfi -i color=c=blue:s=1280x720:d=5 -c:v libx264 temp_video.mp4")
    print("Video generation simulated (temp_video.mp4 created).")
    return "temp_video.mp4"

def merge_audio_video(video_file, audio_file):
    print("Step 4: Merging Audio and Video using FFmpeg...")
    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4"
    os.system(command)
    print("Factory Output Ready: final_video.mp4")

if __name__ == "__main__":
    if not NVIDIA_API_KEY:
        print("Error: NVIDIA_API_KEY not found in environment variables.")
        exit(1)
        
    dialogue, prompt = generate_story_and_prompt()
    
    if dialogue and prompt:
        generate_audio(dialogue)
        vid_file = generate_video(prompt)
        merge_audio_video(vid_file, "audio.mp3")
        print("Automation cycle complete!")
