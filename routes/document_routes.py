from fastapi import APIRouter, HTTPException, Response
from fpdf import FPDF
from typing import List
from pydantic import BaseModel
import io

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class PDFRequest(BaseModel):
    title: str
    messages: List[ChatMessage]

@router.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    """Generate a PDF of the chat history using memory-only processing."""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Set fonts
        pdf.set_font("Helvetica", "B", 16) # Helvetica is reliable
        pdf.cell(0, 15, request.title, ln=True, align="C")
        pdf.ln(10)
        
        for msg in request.messages:
            role = "You" if msg.role == "user" else "GenAI Pro"
            
            # Message Header
            pdf.set_font("Helvetica", "B", 11)
            if msg.role == "user":
                pdf.set_text_color(79, 70, 229) 
            else:
                pdf.set_text_color(16, 185, 129)
            pdf.cell(0, 8, f"{role}:", ln=True)
            
            # Message Body
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(31, 41, 55)
            pdf.multi_cell(0, 5, msg.content.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(4)
            
            # Divider
            pdf.set_draw_color(229, 231, 235)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(4)

        # Output to bytes
        pdf_bytes = pdf.output()
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={request.title.replace(' ', '_')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
