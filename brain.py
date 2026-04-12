import requests
import json

def get_script(topic, gemini_key):
    headers = {'Content-Type': 'application/json'}
    
    # ---------------------------------------------------------
    # THE SMART ENGINE: Google se auto-detect karo working model
    # ---------------------------------------------------------
    working_model = "models/gemini-1.5-flash" # Backup default
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        list_resp = requests.get(list_url).json()
        
        if 'models' in list_resp:
            for m in list_resp['models']:
                # Aisa model dhoondho jo text generate kar sake
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    working_model = m['name']
                    break # Pehla working model milte hi lock kar do
        print(f"🔍 Smart Engine ne yeh model auto-select kiya hai: {working_model}")
    except Exception as e:
        print(f"⚠️ Auto-detect error (using default): {e}")

    # ---------------------------------------------------------
    # CONTENT GENERATION (Using auto-detected model)
    # ---------------------------------------------------------
    url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={gemini_key}"
    
    prompt = f"Write a short, funny 2-line Hindi voiceover script about '{topic}' for an Instagram reel. Also, write a 1-line English prompt to generate a highly detailed, realistic, cinematic 4k image matching the topic. Format output EXACTLY like this:\nHINDI_SCRIPT: [Hindi text]\nIMAGE_PROMPT: [English prompt]"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # Super Loudspeaker
        if 'candidates' not in data:
            print(f"❌ Gemini API ERROR RESPONSE: {data}")
            return None, None
            
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        
        hindi_script = ""
        image_prompt = ""
        
        for line in text_response.split('\n'):
            if line.startswith("HINDI_SCRIPT:"):
                hindi_script = line.replace("HINDI_SCRIPT:", "").strip()
            elif line.startswith("IMAGE_PROMPT:"):
                image_prompt = line.replace("IMAGE_PROMPT:", "").strip()
                
        return hindi_script, image_prompt
        
    except Exception as e:
        print(f"❌ Brain Engine System Error: {e}")
        return None, None
