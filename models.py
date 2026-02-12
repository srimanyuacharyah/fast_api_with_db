from db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class ChatHistory(Base):
    __tablename__ = "chathistory"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    chat_name = Column(String)
    messages = Column(String) # Storing JSON stringified messages
    updated_at = Column(String) # Store as ISO string for simplicity
