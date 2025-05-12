from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Question
from app.schemas import QuestionSchema
from sqlalchemy.sql.expression import func

router = APIRouter(prefix="/interview", tags=["interview"])


@router.get("/questions/random", response_model=List[QuestionSchema])
def get_random_questions(db: Session = Depends(get_db)):
    return db.query(Question).order_by(func.random()).limit(3).all()
