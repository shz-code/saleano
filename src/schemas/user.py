from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserResponse(SQLModel):
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CreateUserRequest(SQLModel):
    username: str
    email: str
    password: str

class UserLoginRequest(SQLModel):
    email: str
    password: str

class TokenResponse(SQLModel):
    access_token: str
    token_type: str