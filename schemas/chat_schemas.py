from pydantic import BaseModel
from typing import List, Optional

class MessageSchema(BaseModel):
    role: str
    content: str
    image: Optional[str] = None

class ChatHistorySchema(BaseModel):
    id: Optional[str] = None
    chat_name: str
    messages: List[MessageSchema]

class ChatListResponse(BaseModel):
    id: str
    chat_name: str
    updated_at: str
