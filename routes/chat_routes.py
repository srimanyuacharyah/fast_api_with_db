from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import ChatHistory
from repositories.chat_repo import ChatRepo
from schemas.chat_schemas import ChatHistorySchema, ChatListResponse, MessageSchema
from utils.jwt_handler import verify_token
from typing import List
import json

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/chats", tags=["chats"])
security = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(auth.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.get("/", response_model=List[ChatListResponse])
def get_user_chats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user.get("sub"))
    chat_repo = ChatRepo(db)
    chats = chat_repo.get_chats_by_user(user_id)
    return [ChatListResponse(id=str(c.id), chat_name=c.chat_name, updated_at=c.updated_at) for c in chats]

@router.get("/{chat_id}", response_model=ChatHistorySchema)
def get_chat_details(chat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    chat_repo = ChatRepo(db)
    db_chat = chat_repo.get_chat_by_id(chat_id)
    if not db_chat or db_chat.user_id != int(current_user.get("sub")):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = json.loads(db_chat.messages)
    return ChatHistorySchema(id=str(db_chat.id), chat_name=db_chat.chat_name, messages=messages)

@router.post("/", response_model=ChatHistorySchema)
def save_chat(chat_data: ChatHistorySchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user.get("sub"))
    chat_repo = ChatRepo(db)
    db_chat = chat_repo.create_or_update_chat(user_id, chat_data)
    
    messages = json.loads(db_chat.messages)
    return ChatHistorySchema(id=str(db_chat.id), chat_name=db_chat.chat_name, messages=messages)

@router.delete("/{chat_id}")
def delete_chat_route(chat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    chat_repo = ChatRepo(db)
    db_chat = chat_repo.get_chat_by_id(chat_id)
    if not db_chat or db_chat.user_id != int(current_user.get("sub")):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat_repo.delete_chat(chat_id)
    return {"message": "Chat deleted successfully"}
