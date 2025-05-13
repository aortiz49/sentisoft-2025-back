from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    b2c: bool
    interview_count: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class QuestionCategorySchema(BaseModel):
    id: int
    category: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    text: str
    category: QuestionCategorySchema

    class Config:
        from_attributes = True


class InterviewAnswerUpdate(BaseModel):
    answer: Optional[str] = None
    clarity_score: Optional[int] = None
    structure_score: Optional[int] = None
    communication_score: Optional[int] = None
    feedback: Optional[str] = None
