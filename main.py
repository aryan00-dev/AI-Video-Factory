import os
import requests
import random
import re
from gtts import gTTS
import fal_client

# API Keys setup
raw_nvidia_key = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_KEY = raw_nvidia_key.replace('\n', '').replace('\r', '').replace(' ', '').strip()

def get_viral_context():
    print("AI Director: Soch raha hai naya topic...")
    topic_pool = {
        "Health & Anatomy": [
            "Pet ka Tezāb (Acid) aur spicy Samosa ki argument",
            "Dil (Heart) aur Dimag (Brain) ki ladai"
        ]
    }
    chosen_category = list(topic_pool.keys())[0]
    chosen_topic = random.choice(topic_pool[chosen_category])
    print(f"Topic mil gaya: {chosen_topic}")
    return f"Category: {chosen_category}, Topic: {chosen_topic}"

def generate_story_and_prompt():
    print("Step 1: NVIDIA (Llama 3) se script maang rahe hain...")
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    viral_context = get_viral_context()
    system_instruction = (
        "You are a viral video creator. Return EXACTLY two lines:\n"
        "Line 1: Hindi dialogue.\n"
        "Line 2: English prompt for 3D video."
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
        
        # --- YAHAN HAI LOUDSPEAKER ---
        print(f"NVIDIA Server ka Jawab (Status Code): {response.status_code}") 
        
        if response.status_code == 200:
            raw_text = response.json()['choices'][0]['message']['content'].strip()
            print(f"NVIDIA ne yeh Script bheji:\n{raw_text}") 
            
            lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
            if len(lines) >= 2:
                dialogue = re.sub(r'^(Line \d+: |Dialogue: |Hindi: )', '', lines[0])
                video_prompt = re.sub(r'^(Line \d+: |Prompt: |English: )', '', lines[1])
                return dialogue, video_prompt
            else:
                print("ERROR: NVIDIA ne 2 line mein script nahi di.")
        else:
            print(f"NVIDIA API ERROR: Dhyan do! Chabi mein ya API mein error hai -> {response.text}")
    except Exception as e:
        print(f"Code ya Internet mein Error: {e}")
    return None, None

def generate_audio(text):
    print("Step 2: Aawaz (Audio) ban rahi hai...")
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save("audio.mp3")
    print("Audio ban gayi.")

def generate_video(prompt):
    print("Step 3: Fal.ai se Asli 3D Video ban rahi hai (Isme 1-2 minute lagenge)...")
    try:
        handler = fal_client.submit(
            "fal-ai/luma-dream-machine",
            arguments={"prompt": prompt, "aspect_ratio": "9:16"},
        )
        result = handler.get()
        video_url = result['video']['url']
        print("Video ban gayi! Download ho rahi hai...")
        vid_data = requests.get(video_url).content
        with open("temp_video.mp4", "wb") as f:
            f.write(vid_data)
        return "temp_video.mp4"
    except Exception as e:
        print(f"Video banane mein ERROR aaya: {e}")
        return None

def merge_audio_video(video_file, audio_file):
    print("Step 4: Video aur Audio ko joda ja raha hai...")
    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4"
    os.system(command)
    print("Badhai Ho! Factory Output Ready: final_video.mp4")

if __name__ == "__main__":
    if not NVIDIA_API_KEY:
        print("ERROR: NVIDIA_API_KEY tijori (Secrets) mein nahi mili!")
        exit(1)
        
    dialogue, prompt = generate_story_and_prompt()
    if dialogue and prompt:
        generate_audio(dialogue)
        vid_file = generate_video(prompt)
        if vid_file:
            merge_audio_video(vid_file, "audio.mp3")
        else:
            print("Video fail ho gayi. Fal.ai ki chabi check karo.")
    else:
        print("Script hi nahi bani, toh aage ka process ruk gaya.")
