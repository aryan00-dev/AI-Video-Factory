import os, requests, re

def get_script(context, key):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "system", "content": "Return 2 lines: Line 1: Hindi dialogue. Line 2: English 3D video prompt."},
            {"role": "user", "content": f"Topic: {context}"}
        ]
    }
    res = requests.post(url, headers=headers, json=payload).json()
    content = res['choices'][0]['message']['content'].strip().split('\n')
    dialogue = re.sub(r'^(Line \d+: |Dialogue: )', '', content[0])
    prompt = re.sub(r'^(Line \d+: |Prompt: )', '', content[1])
    return dialogue, prompt
