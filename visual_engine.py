import requests

def make_image(prompt, hf_key):
    # Naya Updated Hugging Face Router API URL
    API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {hf_key}"}
    
    # Prompt ko aur accha banane ke liye keywords jod rahe hain
    payload = {"inputs": prompt + ", 4k, cinematic lighting, highly detailed, photorealistic"}
    
    try:
        print("📸 Hugging Face ko photo banane ka order ja raha hai...")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            with open("temp_image.png", "wb") as f:
                f.write(response.content)
            print("✅ 4K Photo successfully ban gayi: temp_image.png")
            return "temp_image.png"
        else:
            print(f"❌ Visual Engine Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Visual Engine Crash: {e}")
        return None
