from sqlalchemy.orm import Session
from models import ChatHistory
from schemas.chat_schemas import ChatHistorySchema
import json
from datetime import datetime

class ChatRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_chats_by_user(self, user_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.user_id == user_id).all()

    def get_chat_by_id(self, chat_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()

    def create_or_update_chat(self, user_id: int, chat_data: ChatHistorySchema):
        # Check if chat exists
        db_chat = None
        if chat_data.id:
            db_chat = self.db.query(ChatHistory).filter(ChatHistory.id == int(chat_data.id)).first()

        messages_json = json.dumps([msg.dict() for msg in chat_data.messages])
        now = datetime.utcnow().isoformat()

        if db_chat:
            db_chat.chat_name = chat_data.chat_name
            db_chat.messages = messages_json
            db_chat.updated_at = now
        else:
            db_chat = ChatHistory(
                user_id=user_id,
                chat_name=chat_data.chat_name,
                messages=messages_json,
                updated_at=now
            )
            self.db.add(db_chat)
        
        self.db.commit()
        self.db.refresh(db_chat)
        return db_chat

    def delete_chat(self, chat_id: int):
        db_chat = self.db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
        if db_chat:
            self.db.delete(db_chat)
            self.db.commit()
            return True
        return False
