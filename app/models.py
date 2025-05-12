from sqlalchemy import Boolean, Column, DateTime, Double, Integer, String, func
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy as sa

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(BaseEntity):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    b2c = Column(Boolean, nullable=False, default=True)
    interview_count = Column(Integer, nullable=False, default=0)
    linkedin_url = Column(String, nullable=True)
    clarity_level = Column(Integer, ForeignKey("competency_levels.id"), nullable=True)
    structure_level = Column(Integer, ForeignKey("competency_levels.id"), nullable=True)
    communication_level = Column(
        Integer, ForeignKey("competency_levels.id"), nullable=True
    )
    interviews = relationship(
        "Interviews", back_populates="user", cascade="all, delete-orphan"
    )


class Interviews(BaseEntity):
    __tablename__ = "interviews"
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="interviews")
    questions = relationship(
        "Question", secondary="interview_questions", back_populates="interviews"
    )
    interview_feedback = relationship(
        "InterviewFeedback", back_populates="interview", cascade="all, delete-orphan"
    )


class CompetencyLevel(BaseEntity):
    __tablename__ = "competency_levels"
    __table_args__ = (
        sa.UniqueConstraint("competency", "level", name="uq_competency_level"),
    )
    competency = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(String, nullable=False)


class QuestionCategory(BaseEntity):
    __tablename__ = "question_categories"
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    questions = relationship("Question", back_populates="category")


class Question(BaseEntity):
    __tablename__ = "questions"
    text = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    category = relationship("QuestionCategory", back_populates="questions")
    interviews = relationship(
        "Interviews", secondary="interview_questions", back_populates="questions"
    )


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
    interview = relationship("Interviews", back_populates="interview_feedback")
    mistake_categories = relationship(
        "MistakeCategory",
        secondary="interview_mistakes",
        back_populates="interview_feedbacks",
    )


class MistakeCategory(BaseEntity):
    __tablename__ = "mistake_categories"
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    interview_feedbacks = relationship(
        "InterviewFeedback",
        secondary="interview_mistakes",
        back_populates="mistake_categories",
    )


class InterviewMistake(BaseEntity):
    __tablename__ = "interview_mistakes"
    category_id = Column(Integer, ForeignKey("mistake_categories.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interview_feedback.id"), nullable=False)


class AnalysisRequest(BaseModel):
    question: str
    transcript: str
