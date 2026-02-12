from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
import requests
import io

router = APIRouter()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Using the standard GitHub Models inference endpoint for DALL-E 3
DALL_E_ENDPOINT = "https://models.github.ai/inference/images/generations"

@router.post("/generate-image")
async def generate_image(prompt: str):
    """Generate a real AI image using DALL-E 3 via GitHub Models API."""
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN environment variable is not set")

    try:
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Prepare the payload for DALL-E 3
        payload = {
            "prompt": prompt,
            "model": "dall-e-3",
            "n": 1,
            "size": "1024x1024"
        }

        # Make the request to the AI model
        response = requests.post(DALL_E_ENDPOINT, headers=headers, json=payload)
        
        if response.status_code != 200:
            # Check for common errors like token quota or model availability
            error_data = response.json() if response.content else {"detail": "Unknown API Error"}
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"AI Model Error: {error_data}"
            )

        data = response.json()
        image_url = data.get("data", [{}])[0].get("url")
        
        if not image_url:
            raise HTTPException(status_code=500, detail="AI Model did not return an image URL")

        # Proxy the image bytes to the frontend to maintain session security and the existing UI logic
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            return StreamingResponse(io.BytesIO(image_response.content), media_type="image/png")
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch generated image from source")

    except Exception as e:
        # Fallback or detailed error log
        print(f"Image Generation Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
