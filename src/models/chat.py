from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime
from src.models.user import User

class ChatMessage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    message: str
    response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship back to user
    user: Optional[User] = Relationship(back_populates="messages")