import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_script():
    print("[+] Brain Active: Generating Viral Script...")
    
    # THE "JABARDASTI" FALLBACK SCRIPT 
    fallback_script = "Ruko! Internet par ek aisi secret aur khatarnak AI website aa chuki hai, jo aapke ghanto ka kaam secondon mein free mein kar sakti hai. Yeh tool itna powerful hai ki aapka dimaag kharab ho jayega. Abhi try karo aur apne doston ko shock kar do!"

    if not GROQ_API_KEY:
        print("[-] Warning: GROQ_API_KEY missing! Engaging Jabardasti Fallback Script.")
        with open("current_script.txt", "w", encoding="utf-8") as f:
            f.write(fallback_script)
        return

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = """
        Write a 50-60 word highly engaging Hindi tech script for an Instagram Reel about a crazy, free, and secret AI tool. 
        Rules:
        1. Start exactly with the word "Ruko!". 
        2. Use words like "khatarnak", "secret", "dimaag kharab", "free". 
        3. Do not include emojis, hashtags, or bracketed text. Write pure spoken text only.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", 
            temperature=0.8
        )
        script = chat_completion.choices[0].message.content.strip()
        
        with open("current_script.txt", "w", encoding="utf-8") as f:
            f.write(script)
            
        print("[SUCCESS] Viral Script Ready via Groq.")
        
    except Exception as e:
        print(f"[-] Groq API Failed/Crashed: {e}")
        print("[!] BRAHMASTRA ENGAGED: Forcing Fallback Script. Factory will NOT stop!")
        with open("current_script.txt", "w", encoding="utf-8") as f:
            f.write(fallback_script)

if __name__ == "__main__":
    generate_script()
