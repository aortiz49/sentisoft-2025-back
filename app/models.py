from sqlalchemy import Boolean, Column, DateTime, Double, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
<<<<<<< Updated upstream
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
=======
    b2c = Column(Boolean, nullable=False, default=False)
    interview_count = Column(Integer, nullable=False, default=0)
    linkedin_url = Column(String, nullable=True)
    clarity_level = Column(Integer, ForeignKey("competency_levels.id"), nullable=False)
    structure_level = Column(
        Integer, ForeignKey("competency_levels.id"), nullable=False
    )
    communication_level = Column(
        Integer, ForeignKey("competency_levels.id"), nullable=False
    )


class Interviews(BaseEntity):
    __tablename__ = "interviews"
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class QuestionCategory(BaseEntity):
    __tablename__ = "question_categories"
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Question(BaseEntity):
    __tablename__ = "questions"
    text = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    category = relationship("QuestionCategory", back_populates="questions")


class InterviewQuestion(BaseEntity):
    __tablename__ = "interview_questions"
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)


class InterviewFeedback(BaseEntity):
    __tablename__ = "interview_feedback"
    feedback = Column(String, nullable=False)
    general_score = Column(Double, nullable=False)
    recommendations = Column(String, nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    clarity_level = Column(Integer, ForeignKey("competency_levels.id"), nullable=False)
    structure_level = Column(
        Integer, ForeignKey("competency_levels.id"), nullable=False
    )
    communication_level = Column(
        Integer, ForeignKey("competency_levels.id"), nullable=False
    )


class CompetencyLevel(BaseEntity):
    __tablename__ = "competency_levels"
    competency = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(String, nullable=False)


class MistakeCategory(BaseEntity):
    __tablename__ = "mistake_categories"
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)


class InterviewMistake(BaseEntity):
    __tablename__ = "interview_mistakes"
    category_id = Column(Integer, ForeignKey("mistake_categories.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
>>>>>>> Stashed changes


class AnalysisRequest(BaseModel):
    question: str
    transcript: str
