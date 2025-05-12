from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Question
from app.schemas import QuestionSchema
from sqlalchemy.sql.expression import func
from app.services.auth.auth_services import get_current_user
from app.models import User, Interviews

router = APIRouter(prefix="/interview", tags=["interview"])


@router.get("/questions/random", response_model=List[QuestionSchema])
def get_random_questions(db: Session = Depends(get_db)):
    return db.query(Question).order_by(func.random()).limit(3).all()


@router.post("/new", response_model=dict)
def create_interview_for_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_interview = Interviews(user_id=current_user.id)
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return {
        "interview_id": new_interview.id,
        "user_id": new_interview.user_id,
        "created_at": new_interview.created_at,
        "updated_at": new_interview.updated_at,
    }
