from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.schemas.user import UserResponse

class ChatMessageResponse(SQLModel):
    id: UUID
    user_id: UUID
    message: str
    response: Optional[str]
    timestamp: datetime

class CreateChatMessageRequest(SQLModel):
    message: str

class ChatMessageWithUserResponse(SQLModel):
    id: UUID
    message: str
    response: Optional[str]
    timestamp: datetime
    user: UserResponse