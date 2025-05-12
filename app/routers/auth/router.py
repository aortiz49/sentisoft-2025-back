from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Depends
import os
from app.schemas import UserCreate, UserRead, Token
from app.models import User
from app.services.auth.auth_services import (
    get_password_hash,
    get_user_by_email,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


@router.post("/register", response_model=UserRead)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already registered")
    hashed = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form: UserCreate,  # or OAuth2PasswordRequestForm
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form.email, form.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_EXPIRE),
    )
    return {"access_token": access_token}


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user
