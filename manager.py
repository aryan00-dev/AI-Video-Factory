import os
import google.generativeai as genai
from duckduckgo_search import DDGS

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[-] Error: GEMINI_API_KEY missing!")
    exit(1)

genai.configure(api_key=API_KEY)

def get_latest_news():
    print("[+] Radar Active: Scanning Open Web...")
    news_data = ""
    try:
        with DDGS() as ddgs:
            results = ddgs.text("new open source AI tools", max_results=3)
            for r in results: news_data += f"- {r['title']}\n"
    except: pass
    return news_data

def generate_viral_script(news_data):
    print("[+] Brain Active: Generating 60-Word Script...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Tum ek expert AI Tech Video creator ho.
    News: {news_data}
    Ek aggressive Hinglish short video script likho.
    RULES:
    1. Hook humesha FOMO se start ho (e.g., "Ruko! Agar tum abhi bhi purane tools use kar rahe ho...").
    2. Exact word count: 55 se 65 words ke beech.
    3. Tool ka naam aur "Free" nature highlight karo.
    4. Har 2 sentence ke baad ek shock factor ho.
    Sirf spoken text do.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace('*', '').replace('"', '')
    except:
        return "Ruko! Agar tum abhi bhi ChatGPT use kar rahe ho, toh tumhara dimaag kharab hone wala hai. Yeh naya secret AI tool market mein aag laga raha hai aur yeh free hai. Iska naam hai Qwen aur yeh tumhare ghanto ka kaam second mein karta hai. Abhi try karo."

if __name__ == "__main__":
    news = get_latest_news()
    script = generate_viral_script(news)
    with open("current_script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print(f"[SUCCESS] Viral Script Ready.")
