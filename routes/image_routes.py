from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import io
import random

router = APIRouter()

@router.post("/generate-image")
async def generate_image(prompt: str):
    """Generate a stylized abstract image using memory-only processing for maximum speed."""
    try:
        # Optimized size for quick generation and low bandwidth
        width, height = 512, 512
        image = Image.new("RGB", (width, height), "#0f172a")
        draw = ImageDraw.Draw(image)
        
        colors = ["#4f46e5", "#7c3aed", "#10b981", "#3b82f6", "#f43f5e"]
        random.seed(prompt) # Consistent image for same prompt
        
        # High-speed abstract drawing
        for _ in range(10):
            shape_type = random.choice(["circle", "line", "rectangle"])
            color = random.choice(colors)
            
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(width // 4, width)
            y2 = random.randint(height // 4, height)
            
            if shape_type == "circle":
                r = random.randint(10, 60)
                draw.ellipse([x1-r, y1-r, x1+r, y1+r], outline=color, width=2)
            elif shape_type == "line":
                draw.line([x1, y1, x2, y2], fill=color, width=2)
            else:
                draw.rectangle([x1, y1, x2, y2], outline=color, width=1)

        # Subtle branding
        try:
            font = ImageFont.load_default()
            draw.text((15, 480), "GenAI Pro Instant Visual", fill="#6366f1", font=font)
        except:
            pass

        # Save to memory instead of disk
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
