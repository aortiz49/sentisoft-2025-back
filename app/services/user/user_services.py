from app.models import User
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Optional


def get_user_by_id(user_id: int, db: Session = None) -> Optional[User]:
    db = db or get_db()
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(email: str, db: Session = None) -> Optional[User]:
    db = db or get_db()
    return db.query(User).filter(User.email == email).first()


def update_user_profile(user_id: int, **kwargs) -> Optional[User]:
    """Update user profile information"""
    db = get_db()
    user = get_user_by_id(user_id, db)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def get_user_interviews(user_id: int) -> list:
    """Get all interviews for a user"""
    db = get_db()
    user = get_user_by_id(user_id, db)
    if user:
        return user.interviews
    return []
