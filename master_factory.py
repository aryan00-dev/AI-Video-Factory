import os
import random
import requests
from gtts import gTTS
from moviepy.editor import *
from moviepy.audio.fx.all import audio_loop
from playwright.sync_api import sync_playwright
from duckduckgo_search import DDGS

HF_KEY = os.environ.get("HUGGINGFACE_KEY")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko", "tool"]

# ==========================================
# PART 1: ASSETS & VIRTUAL SCREEN RECORDING
# ==========================================
def fetch_and_record_website():
    print("[+] Fetching Assets & Recording Screen Virtually...")
    assets = {'meme': False, 'audio': False, 'recording': False}
    
    # 1. Fetch Meme Hook
    try:
        res = requests.get("https://api.imgflip.com/get_memes", timeout=10).json()
        meme = random.choice(res['data']['memes'][:20])
        req = requests.get(meme['url'], headers=HEADERS, timeout=10)
        if len(req.content) > 1000:
            with open('live_meme.png', 'wb') as f: f.write(req.content)
            assets['meme'] = True
    except: pass

    # 2. Fetch Lo-Fi BGM & Pop Sound
    try:
        bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
        pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
        bgm_req = requests.get(bgm_url, headers=HEADERS, timeout=10)
        pop_req = requests.get(pop_url, headers=HEADERS, timeout=10)
        if len(bgm_req.content) > 5000:
            with open('live_bgm.ogg', 'wb') as f: f.write(bgm_req.content)
            with open('live_pop.ogg', 'wb') as f: f.write(pop_req.content)
            assets['audio'] = True
    except: pass

    # 3. Virtual Screen Recording Engine (Playwright)
    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script_text = f.read().lower()
        
        # Searching the tool website
        query = " ".join(script_text.split()[:10]) + " official tool website"
        tool_url = "https://huggingface.co/spaces" # Backup Tech Vibe URL
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=1):
                    tool_url = r['href']
                    break
        except: pass
        
        print(f"[+] Recording Target: {tool_url}")
        
        # Virtual Browser Recording
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(record_video_dir="./", record_video_size={"width": 1080, "height": 1920}, viewport={"width": 1080, "height": 1920})
            page = context.new_page()
            
            try:
                page.goto(tool_url, wait_until="load", timeout=15000)
            except: pass # If page loads slow, keep recording whatever is there
            
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, -200)
            page.wait_for_timeout(1000)
            
            video_path = page.video.path()
            context.close() # CRITICAL: Finalizes the video saving process
            browser.close()
            
            os.rename(video_path, 'live_web_recording.mp4')
            assets['recording'] = True
            print("[+] Virtual Screen Recorded Successfully.")
    except Exception as e:
        print(f"[-] Recording Failed: {e}")
        exit(1) # Majbur Rule: Halt factory if recording fails to prevent trash videos.

    return assets

def get_voice(text, filename="audio.mp3"):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    try:
        res = requests.post(API_URL, headers={"Authorization": f"Bearer {HF_KEY}"}, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f: f.write(res.content)
            return
    except: pass
    gTTS(text=text, lang='hi', slow=False).save(filename)

# ==========================================
# PART 2: CORE FACTORY EDITOR
# ==========================================
def build_video():
    assets = fetch_and_record_website()
    
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    
    audio_elements = [voice_clip]
    valid_audio = False
    
    if assets['audio']:
        try:
            base_bgm = AudioFileClip("live_bgm.ogg").volumex(0.15)
            bgm_clip = audio_loop(base_bgm, duration=total_duration)
            base_pop_sfx = AudioFileClip("live_pop.ogg").volumex(0.6)
            audio_elements.append(bgm_clip)
            valid_audio = True
        except: pass

    visual_elements = []

    # 1. Screen Recording Background (Looped to match audio)
    if assets['recording']:
        web_clip = (VideoFileClip("live_web_recording.mp4")
                   .volumex(0)
                   .loop(duration=total_duration)
                   .set_duration(total_duration))
        # Dark overlay to make text pop
        dark_overlay = ColorClip(size=(1080, 1920), color=(10, 10, 15)).set_opacity(0.6).set_duration(total_duration)
        visual_elements.extend([web_clip, dark_overlay])

    # 2. Meme Hook (Slide up animation)
    if assets['meme']:
        try:
            meme_clip = (ImageClip("live_meme.png")
                         .resize(width=800)
                         .set_position(lambda t: ('center', int(min(960, 1920 - 1500*t))))
                         .set_start(0)
                         .set_duration(2.5)
                         .crossfadeout(0.3))
            visual_elements.append(meme_clip)
        except: pass

    # 3. Dynamic Bouncy Typography (With Stroke)
    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        if len(clean) > 5 or clean in POWER_WORDS:
            color = "yellow"
            font_size = 150
            if valid_audio:
                pop_sfx = base_pop_sfx.set_start(current_time)
                audio_elements.append(pop_sfx)
        else:
            color = "white"
            font_size = 110
            
        txt = (TextClip(word, fontsize=font_size, color=color, 
                        stroke_color='black', stroke_width=4,
                        font='DejaVu-Sans-Bold', method='caption', size=(950, None))
               .set_position(('center', 'center'))
               .set_start(current_time)
               .set_duration(time_per_word))
               
        visual_elements.append(txt)
        current_time += time_per_word

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)

    print("[+] Rendering Base Masterpiece...")
    final_video.write_videofile("temp_video.mp4", fps=30, codec="libx264", audio_codec="aac")

    # PART 3: FFMPEG 1.25x HIGH ENERGY INJECTOR
    print("[+] Injecting High Energy via FFmpeg...")
    os.system("ffmpeg -y -i temp_video.mp4 -filter_complex \"[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]\" -map \"[v]\" -map \"[a]\" final_tech_viral_video.mp4")

    print("[SUCCESS] Creator's Masterpiece Rendered!")

if __name__ == "__main__":
    build_video()
