from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from src.db import get_session
from src.models.chat import ChatMessage
from src.models.user import User
from src.schemas.chat import ChatMessageResponse, CreateChatMessageRequest
from src.lib.auth import get_current_user
from src.constants import API_VERSION

router = APIRouter(prefix=f"/api/{API_VERSION}/chat", tags=["Chat"])

@router.get("/", response_model=List[ChatMessageResponse])
def get_chat_messages(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    messages = session.exec(
        select(ChatMessage).where(ChatMessage.user_id == current_user.id)
    ).all()
    return messages

@router.post("/", response_model=ChatMessageResponse)
def create_chat_message(
    message_data: CreateChatMessageRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # For now, just echo the message as response. In a real app, you'd integrate with an AI service.
    response = f"Echo: {message_data.message}"

    db_message = ChatMessage(
        user_id=current_user.id,
        message=message_data.message,
        response=response
    )
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message