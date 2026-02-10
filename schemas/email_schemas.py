from pydantic import BaseModel

class EmailSchema(BaseModel):
    receiver_email: str
    subject: str
    content: str
