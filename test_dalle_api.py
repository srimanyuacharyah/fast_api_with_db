import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DALL_E_ENDPOINT = "https://models.github.ai/inference/images/generations"

def test_dalle():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not found in environment")
        return

    print(f"Using Token: {GITHUB_TOKEN[:10]}...")
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": "royal palace",
        "model": "dall-e-3",
        "n": 1,
        "size": "1024x1024"
    }

    try:
        print(f"Requesting {DALL_E_ENDPOINT}...")
        response = requests.post(DALL_E_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response Content:")
        print(response.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_dalle()
