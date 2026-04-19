import os
import google.generativeai as genai

# GitHub Secrets se API Key uthana
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("[-] Error: GEMINI_API_KEY nahi mili!")
    exit(1)

genai.configure(api_key=API_KEY)

# Gemini Model ko wild topic sochne ka command
model = genai.GenerativeModel('gemini-1.5-flash') # Fast model for quick topic generation
prompt = """Tum ek highly creative comedy aur roasting writer ho. 
Mujhe 'Object Roasting' ke liye ek bilkul naya, ajeeb aur wild topic do jo aaj tak kisi ne na socha ho.
Limitless raho (e.g., Space, History, Daily items, Emotions).
Format strictly yahi hona chahiye: [Object 1] roasting [Object 2].
Example: 'Ek Tuta hua Kanch roasting a Diamond', 'Black Hole roasting a Torch light'.
Sirf aur sirf topic ka naam likho, koi extra word nahi."""

try:
    response = model.generate_content(prompt)
    topic = response.text.strip()
    
    with open("current_topic.txt", "w", encoding="utf-8") as f:
        f.write(topic)
        
    print(f"[+] Limitless Manager: Aaj ka wild topic hai -> {topic}")
except Exception as e:
    print(f"[-] Topic generate karne mein error aaya: {e}")
