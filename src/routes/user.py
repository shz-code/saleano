from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.db import get_session
from src.models.user import User
from src.schemas.user import UserResponse, CreateUserRequest, UserLoginRequest, TokenResponse
from src.lib.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from src.constants import API_VERSION
from datetime import timedelta

router = APIRouter(prefix=f"/api/{API_VERSION}/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: CreateUserRequest, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(
        select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLoginRequest, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user