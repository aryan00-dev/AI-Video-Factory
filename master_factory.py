jimport os
import random
import requests
from gtts import gTTS
from moviepy.editor import *

HF_KEY = os.environ.get("HUGGINGFACE_KEY")

THEMES = [
    {"name": "Hacker", "bg": (10, 15, 10), "power": "yellow", "normal": "white"},
    {"name": "Synthwave", "bg": (20, 5, 20), "power": "cyan", "normal": "white"},
    {"name": "Alert", "bg": (15, 5, 5), "power": "red", "normal": "white"}
]
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt"]

def get_voice(text, filename="audio.mp3"):
    print("[+] Calling Hugging Face Open-Source Voice...")
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    try:
        res = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(res.content)
            print("[+] Voice Generation Successful via HF!")
            return
    except Exception as e:
        print(f"[-] HF Server Timeout. Error: {e}")
        
    print("[!] Fallback: Using gTTS Backup...")
    gTTS(text=text, lang='hi', slow=False).save(filename)

def build_video():
    print("[SYSTEM] Final Master Editor (Asset Vault Edition) Initiated...")
    
    # 1. Read Script
    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script = f.read().strip()
    except:
        script = "Agar tum abhi bhi ChatGPT use kar rahe ho, toh tum bohot peeche ho. Yeh naya free AI tool khatarnak hai."
        
    # 2. Setup Base Audio
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    
    # Audio Manager List (Voice + BGM + SFX)
    audio_elements = [voice_clip]
    
    # Add BGM if exists in Asset Vault
    if os.path.exists("assets/bgm.mp3"):
        print("[+] Asset Vault: Loading BGM...")
        bgm_clip = AudioFileClip("assets/bgm.mp3").volumex(0.1).set_duration(total_duration)
        audio_elements.append(bgm_clip)

    # 3. Setup Vibe & Visuals
    theme = random.choice(THEMES)
    bg_clip = ColorClip(size=(1080, 1920), color=theme["bg"], duration=total_duration)
    
    visual_elements = [bg_clip]
    
    # Add Cat Meme at the beginning (0 to 2 seconds) if exists
    if os.path.exists("assets/cat.png"):
        print("[+] Asset Vault: Loading Cat Reaction Meme...")
        meme_clip = (ImageClip("assets/cat.png")
                     .set_duration(2)
                     .resize(width=600)
                     .set_position(('center', 'bottom'))
                     .crossfadein(0.2))
        visual_elements.append(meme_clip)

    # 4. Typography Math & SFX Sync
    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        
        if len(clean) > 5 or clean in POWER_WORDS:
            color, size = theme["power"], 140
            
            # Sync Pop Sound Effect for Power Words
            if os.path.exists("assets/pop.mp3"):
                pop_sfx = AudioFileClip("assets/pop.mp3").volumex(0.5).set_start(current_time)
                audio_elements.append(pop_sfx)
        else:
            color, size = theme["normal"], 90
            
        txt = (TextClip(word, fontsize=size, color=color, font='Arial-Bold', method='caption', size=(900, None))
               .set_position(('center', 'center'))
               .set_start(current_time)
               .set_duration(time_per_word)
               .crossfadein(0.05)) # Bounce/Pop visual effect
               
        visual_elements.append(txt)
        current_time += time_per_word

    # 5. Final Assembly
    print("[+] Assembling Video, Audio & Effects...")
    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)
    
    output_name = "final_tech_viral_video.mp4"
    final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    print(f"[SUCCESS] Video Rendered and Ready: {output_name}")

if __name__ == "__main__":
    build_video()
