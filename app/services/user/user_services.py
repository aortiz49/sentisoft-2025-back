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


def get_current_user(token: str) -> Optional[User]:
    """Get current user from JWT token"""
    try:
        # Decode the token to get the user's email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            return None

        # Get the user from the database
        db = get_db()
        return get_user_by_email(email, db)

    except JWTError:
        return None


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
