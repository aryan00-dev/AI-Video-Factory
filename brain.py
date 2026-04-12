import requests
import json

def get_script(topic, gemini_key):
    headers = {'Content-Type': 'application/json'}
    
    # Smart Engine: Auto-detect working model
    working_model = "models/gemini-1.5-flash"
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        list_resp = requests.get(list_url).json()
        
        if 'models' in list_resp:
            for m in list_resp['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    working_model = m['name']
                    break
        print(f"🔍 Smart Engine ne yeh model select kiya: {working_model}")
    except Exception as e:
        print(f"⚠️ Auto-detect error, default chalega.")

    # Content Generation
    url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={gemini_key}"
    
    prompt = f"Write a short, funny 2-line Hindi voiceover script about '{topic}' for an Instagram reel. Also, write a 1-line English prompt to generate a highly detailed, realistic, cinematic 4k image matching the topic. Format output EXACTLY like this:\nHINDI_SCRIPT: [Hindi text]\nIMAGE_PROMPT: [English prompt]"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'candidates' not in data:
            print(f"❌ Gemini API ERROR RESPONSE: {data}")
            return None, None
            
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        print(f"📝 RAW AI RESPONSE:\n{text_response}\n-------------------")
        
        hindi_script = ""
        image_prompt = ""
        
        # Bulletproof Parser: Stars (**) aur extra spaces ka asar khatam
        for line in text_response.split('\n'):
            clean_line = line.replace('**', '').strip()
            if "HINDI_SCRIPT:" in clean_line:
                hindi_script = clean_line.split("HINDI_SCRIPT:")[-1].strip()
            elif "IMAGE_PROMPT:" in clean_line:
                image_prompt = clean_line.split("IMAGE_PROMPT:")[-1].strip()
                
        if not hindi_script or not image_prompt:
             print("❌ ERROR: Format mismatch. Text theek se nahi nikla.")
                
        return hindi_script, image_prompt
        
    except Exception as e:
        print(f"❌ Brain Engine System Error: {e}")
        return None, None
