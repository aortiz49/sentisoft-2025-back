# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    if auth.get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form: schemas.UserCreate,  # or OAuth2PasswordRequestForm
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form.email, form.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=auth.ACCESS_EXPIRE),
    )
    return {"access_token": access_token}


@router.get("/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
