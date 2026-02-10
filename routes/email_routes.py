from fastapi import APIRouter
from utils.email_sender import send_email

router = APIRouter()


@router.post("/send-email")
def send_email_route(email: str, subject: str, content: str):
    """Send an email to the receiver with the given subject and content."""
    send_email(email, subject, content)
    return {"message": "Email sent successfully"}