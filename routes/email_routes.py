from fastapi import APIRouter, HTTPException
from utils.email_sender import send_email
from schemas.email_schemas import EmailSchema

router = APIRouter()


@router.post("/send-email")
def send_email_route(request: EmailSchema):
    """Send an email to the receiver with the given subject and content."""
    try:
        send_email(request.receiver_email, request.subject, request.content)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))