from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
import sqlalchemy as sa
from datetime import datetime

from app.models import Interviews, Question, InterviewQuestion, User
from app.schemas import QuestionSchema
from app.database import get_db
from app.services.auth.auth_services import get_current_user

router = APIRouter(prefix="/interview", tags=["interview"])


@router.patch("/{interview_id}/question/{question_id}", response_model=dict)
def update_interview_question_answer(
    interview_id: int,
    question_id: int,
    answer: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Optional: confirm interview belongs to current user
    interview = (
        db.query(Interviews)
        .filter(Interviews.id == interview_id, Interviews.user_id == current_user.id)
        .first()
    )
    if not interview:
        raise HTTPException(
            status_code=404, detail="Interview not found or unauthorized"
        )

    # Find the interview-question link
    iq = (
        db.query(InterviewQuestion)
        .filter_by(interview_id=interview_id, question_id=question_id)
        .first()
    )
    if not iq:
        raise HTTPException(
            status_code=404, detail="Question not found in this interview"
        )

    iq.answered_at = datetime.utcnow()
    iq.answer = answer
    db.commit()
    db.refresh(iq)

    return {
        "interview_id": interview_id,
        "question_id": question_id,
        "answered_at": iq.answered_at.isoformat(),
        "answer": iq.answer,
    }


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
