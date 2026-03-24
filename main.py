import os
import requests
import random
import re
from gtts import gTTS
import fal_client

# API Keys setup
raw_nvidia_key = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_KEY = raw_nvidia_key.replace('\n', '').replace('\r', '').replace(' ', '').strip()

# ==========================================================
# The AI Director
# ==========================================================
def get_viral_context():
    print("AI Director: Choosing a trendy topic...")
    topic_pool = {
        "Health & Anatomy": [
            "Pet ka Tezāb (Acid) aur spicy Samosa ki argument",
            "Dil (Heart) aur Dimag (Brain) ki ladai lifestyle ko lekar",
            "Toot-te baalon (Hair fall) ka dukh"
        ],
        "Trending Comedy": [
            "Jalebi and Burger comparing their popularity",
            "A Mobile screen arguing with its owner"
        ]
    }
    chosen_category = random.choice(list(topic_pool.keys()))
    chosen_topic = random.choice(topic_pool[chosen_category])
    print(f"Topic selected: {chosen_topic}")
    return f"Category: {chosen_category}, Topic: {chosen_topic}"

# ==========================================================
# Step 1: Script & Prompt
# ==========================================================
def generate_story_and_prompt():
    print("Step 1: Asking Llama-3 for a Viral Script...")
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    viral_context = get_viral_context()
    system_instruction = (
        "You are a top viral video creator for Instagram. "
        "Return EXACTLY two lines, no extra text:\n"
        "Line 1: One funny Hindi dialogue (Latin script like Hinglish) for the character.\n"
        "Line 2: One descriptive English prompt for a 3D video generator (Pixar style) depicting this scene."
    )
    
    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Write a script about: {viral_context}"}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            lines = [line.strip() for line in response.json()['choices'][0]['message']['content'].strip().split('\n') if line.strip()]
            if len(lines) >= 2:
                dialogue = re.sub(r'^(Line \d+: |Dialogue: |Hindi: )', '', lines[0])
                video_prompt = re.sub(r'^(Line \d+: |Prompt: |English: )', '', lines[1])
                print(f"Dialogue: {dialogue}")
                print(f"Prompt: {video_prompt}")
                return dialogue, video_prompt
    except Exception as e:
        print(f"Error in Script Generation: {e}")
    return None, None

# ==========================================================
# Step 2: Audio (TTS)
# ==========================================================
def generate_audio(text):
    print("Step 2: Generating Audio (TTS)...")
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save("audio.mp3")
        print("Audio generated successfully.")
    except Exception as e:
        print(f"Error in TTS: {e}")

# ==========================================================
# Step 3: REAL Video Generation (Fal.ai -> Luma Dream Machine)
# ==========================================================
def generate_video(prompt):
    print("Step 3: Generating REAL 3D Video via Fal.ai (This takes 1-2 minutes)...")
    try:
        # Luma Dream Machine endpoint par prompt bhej rahe hain
        handler = fal_client.submit(
            "fal-ai/luma-dream-machine",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "9:16" # Instagram Reel Size
            },
        )
        result = handler.get()
        video_url = result['video']['url']
        print(f"Video generated! Downloading from Fal.ai...")
        
        # Download the MP4 file
        vid_data = requests.get(video_url).content
        with open("temp_video.mp4", "wb") as f:
            f.write(vid_data)
        print("temp_video.mp4 saved.")
        return "temp_video.mp4"
    except Exception as e:
        print(f"Error in Video Generation: {e}")
        return None

# ==========================================================
# Step 4: Merging
# ==========================================================
def merge_audio_video(video_file, audio_file):
    print("Step 4: Merging Audio and Video...")
    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4"
    os.system(command)
    print("Factory Output Ready: final_video.mp4")

if __name__ == "__main__":
    if not NVIDIA_API_KEY:
        print("Error: NVIDIA_API_KEY missing.")
        exit(1)
        
    dialogue, prompt = generate_story_and_prompt()
    if dialogue and prompt:
        generate_audio(dialogue)
        vid_file = generate_video(prompt)
        if vid_file:
            merge_audio_video(vid_file, "audio.mp3")
            print("100% Automation cycle complete!")
        else:
            print("Video generation failed. API credits might be empty.")
