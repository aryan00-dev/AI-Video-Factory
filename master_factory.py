import os
import random
import requests
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.all as vfx
from moviepy.audio.fx.all import audio_loop

HF_KEY = os.environ.get("HUGGINGFACE_KEY")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

THEMES = [
    {"name": "Hacker", "bg": (10, 15, 10), "power": "yellow", "normal": "white"},
    {"name": "Synthwave", "bg": (20, 5, 20), "power": "cyan", "normal": "white"},
    {"name": "Alert", "bg": (15, 5, 5), "power": "red", "normal": "white"}
]
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko"]

def fetch_live_meme():
    try:
        res = requests.get("https://api.imgflip.com/get_memes", timeout=10).json()
        meme = random.choice(res['data']['memes'][:20])
        req = requests.get(meme['url'], headers=HEADERS, timeout=10)
        if len(req.content) > 1000: # Check if valid image
            with open('live_meme.png', 'wb') as f: f.write(req.content)
            return True
        return False
    except: return False

def fetch_live_audio():
    bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
    pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
    try:
        bgm_req = requests.get(bgm_url, headers=HEADERS, timeout=10)
        pop_req = requests.get(pop_url, headers=HEADERS, timeout=10)
        # Shield: Check if Wikipedia sent actual audio or junk text
        if len(bgm_req.content) > 5000 and len(pop_req.content) > 1000:
            with open('live_bgm.ogg', 'wb') as f: f.write(bgm_req.content)
            with open('live_pop.ogg', 'wb') as f: f.write(pop_req.content)
            return True
        return False
    except: return False

def get_voice(text, filename="audio.mp3"):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    try:
        res = requests.post(API_URL, headers={"Authorization": f"Bearer {HF_KEY}"}, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f: f.write(res.content)
            return
    except: pass
    gTTS(text=text, lang='hi', slow=False).save(filename)

def build_video():
    has_meme = fetch_live_meme()
    has_audio = fetch_live_audio()
    
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    
    audio_elements = [voice_clip]
    valid_audio = False
    
    # THE SHIELD: Testing audio file before using it to prevent crash
    if has_audio:
        try:
            base_bgm = AudioFileClip("live_bgm.ogg").volumex(0.1)
            bgm_clip = audio_loop(base_bgm, duration=total_duration)
            base_pop_sfx = AudioFileClip("live_pop.ogg").volumex(0.5)
            audio_elements.append(bgm_clip)
            valid_audio = True
            print("[+] Audio Vault Loaded Successfully.")
        except Exception as e:
            print(f"[!] Shield Activated: Third-party audio corrupted. Bypassing to save factory. Error: {e}")
            valid_audio = False

    theme = random.choice(THEMES)
    bg_clip = ColorClip(size=(1080, 1920), color=theme["bg"], duration=total_duration)
    visual_elements = [bg_clip]
    
    if has_meme:
        try:
            meme_clip = (ImageClip("live_meme.png").set_duration(2.5).resize(width=700)
                         .set_position(('center', 'bottom')).crossfadein(0.2).crossfadeout(0.2))
            visual_elements.append(meme_clip)
        except: pass

    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        if len(clean) > 5 or clean in POWER_WORDS:
            color, size = theme["power"], 145
            if valid_audio:
                pop_sfx = base_pop_sfx.set_start(current_time)
                audio_elements.append(pop_sfx)
        else:
            color, size = theme["normal"], 90
            
        txt = (TextClip(word, fontsize=size, color=color, font='DejaVuSans-Bold', method='caption', size=(900, None))
               .set_position(('center', 'center')).set_start(current_time).set_duration(time_per_word))
        visual_elements.append(txt)
        current_time += time_per_word

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)

    # Auto-Speed Math to prevent timing errors
    if final_video.duration < 25 or final_video.duration > 35:
        factor = final_video.duration / 30.0
        final_video = final_video.fx(vfx.speedx, factor)

    final_video.write_videofile("final_tech_viral_video.mp4", fps=30, codec="libx264", audio_codec="aac")
    print("[SUCCESS] Nirmata Factory Render Complete! Zero Errors.")

if __name__ == "__main__":
    build_video()
