from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import sqlalchemy as sa

from app.models import Interviews, Question, InterviewQuestion, User
from app.schemas import QuestionSchema
from app.database import get_db
from app.services.auth.auth_services import get_current_user

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/new", response_model=dict)
def generate_interview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1: Pick 3 random questions
    questions: List[Question] = (
        db.query(Question).order_by(sa.func.random()).limit(3).all()
    )
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available")

    # Step 2: Create new interview
    interview = Interviews(user_id=current_user.id)
    db.add(interview)
    db.flush()  # ensures interview.id is available

    # Step 3: Link questions to interview
    for question in questions:
        iq = InterviewQuestion(
            interview_id=interview.id,
            question_id=question.id,
        )
        db.add(iq)

    db.commit()
    db.refresh(interview)

    return {
        "interview_id": str(interview.id),
        "questions": [QuestionSchema.from_orm(q) for q in questions],
    }
