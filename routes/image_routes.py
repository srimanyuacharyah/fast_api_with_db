from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import io
import random
from openai import OpenAI
from dotenv import load_dotenv

router = APIRouter()

# Load environment variables
load_dotenv()

@router.post("/generate-image")
async def generate_image(prompt: str):
    """
    Generate an image. 
    Attempts to use DALL-E 3 via GitHub Models first.
    Falls back to a high-quality local stylized generation if the API fails.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    
    # Try Cloud Generation First
    if github_token:
        try:
            client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token,
            )

            # Different potential model IDs to try
            model_id = "openai/dall-e-3" 
            
            response = client.images.generate(
                model=model_id,
                prompt=prompt,
                n=1,
                size="1024x1024",
                timeout=15.0 # Don't hang the request forever
            )

            image_url = response.data[0].url
            if image_url:
                image_response = requests.get(image_url, timeout=10.0)
                if image_response.status_code == 200:
                    return StreamingResponse(io.BytesIO(image_response.content), media_type="image/png")
        except Exception as e:
            print(f"Cloud Image Generation failed (falling back to local): {e}")

    # Fallback: High-Quality Local Stylized Generation
    try:
        width, height = 1024, 1024
        # Create a deep gradient background
        image = Image.new("RGB", (width, height), "#0f172a")
        draw = ImageDraw.Draw(image)
        
        # Premium color palette
        colors = ["#4f46e5", "#7c3aed", "#10b981", "#3b82f6", "#f43f5e", "#fbbf24"]
        random.seed(prompt)
        
        # Draw a lot of abstract shapes for a "generative art" look
        for _ in range(30):
            shape_type = random.choice(["circle", "line", "rectangle", "curve"])
            color = random.choice(colors)
            opacity = random.randint(50, 200)
            
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            
            if shape_type == "circle":
                r = random.randint(20, 150)
                draw.ellipse([x1-r, y1-r, x1+r, y1+r], outline=color, width=random.randint(2, 5))
            elif shape_type == "line":
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 4))
            elif shape_type == "rectangle":
                # Ensure ordered coordinates
                draw.rectangle([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)], outline=color, width=random.randint(1, 3))
            else:
                # Abstract dots
                draw.point([x1, y1, x2, y2], fill=color)

        # Subtle branding/text overlay
        try:
            # Attempt to load a default font
            font = ImageFont.load_default()
            draw.text((20, height - 40), f"GenAI Pro: {prompt[:50]}...", fill="#6366f1", font=font)
        except:
            pass

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        print(f"Local fallback also failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed completely: {str(e)}")
