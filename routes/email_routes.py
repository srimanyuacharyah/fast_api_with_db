from fastapi import APIRouter
from utils.email_sender import send_email
from schemas.email_schemas import EmailSchema

router = APIRouter()


@router.post("/send-email")
def send_email_route(email_data: EmailSchema):
    """Send an email to the receiver with the given subject and content."""
    send_email(email_data.receiver_email, email_data.subject, email_data.content)
    return {"message": "Email sent successfully"}