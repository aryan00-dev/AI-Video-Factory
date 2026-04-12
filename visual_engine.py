import requests

def make_image(prompt, hf_key):
    # CORRECT & UPDATED ROUTER URL
    API_URL = "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {hf_key}"}
    
    payload = {"inputs": prompt + ", cinematic lighting, highly detailed, photorealistic, 4k resolution"}
    
    try:
        print("📸 Hugging Face ko photo banane ka order ja raha hai...")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            with open("temp_image.png", "wb") as f:
                f.write(response.content)
            print("✅ Photo successfully ban gayi: temp_image.png")
            return "temp_image.png"
        # Handling Model Loading (503)
        elif response.status_code == 503:
            print("⏳ Model load ho raha hai... 1 minute baad dobara Run Workflow dabana.")
            return None
        else:
            print(f"❌ Visual Engine Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Visual Engine Crash: {e}")
        return None
