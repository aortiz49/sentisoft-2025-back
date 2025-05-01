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
    interviews = relationship("Interviews", back_populates="user", cascade="all, delete-orphan")
    scorecodes = relationship("ScoreCode", secondary="user_scorecode", back_populates="users")


class Interviews(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="interviews")
    questions = relationship("Question", secondary="interview_questions", back_populates="interviews")
    interview_feedback = relationship("InterviewFeedback", back_populates="interview", cascade="all, delete-orphan")
    scorecodes = relationship("ScoreCode", secondary="interview_scorecodes", back_populates="interviews")

class QuestionCategory(Base):
    __tablename__ = "question_categories"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    category = relationship("QuestionCategory", back_populates="questions")
    interviews = relationship("Interviews", secondary="interview_questions", back_populates="questions")
    
class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)

class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"
    id = Column(Integer, primary_key=True, index=True)
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
    mistake_categories = relationship("MistakeCategory", secondary="interview_mistakes", back_populates="interview_feedbacks")
    
class CompetencyLevel(Base):
    __tablename__ = "competency_levels"
    id = Column(Integer, primary_key=True, index=True)
    competency = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(String, nullable=False)


class MistakeCategory(Base):
    __tablename__ = "mistake_categories"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)


class InterviewMistake(Base):
    __tablename__ = "interview_mistakes"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("mistake_categories.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)

class ScoreCode(Base):
    __tablename__ = "score_codes"
    id = Column(Integer, primary_key=True, index=True)
    competency = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(String, nullable=False)
    users = relationship("User", secondary="user_scorecode", back_populates="scorecodes")
    interviews = relationship("Interviews", secondary="interview_scorecodes", back_populates="scorecodes")

class UserScoreCode(Base):
    __tablename__ = "user_scorecode"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    score_code_id = Column(Integer, ForeignKey("score_codes.id"), primary_key=True)

class InterviewScoreCode(Base):
    __tablename__ = "interview_scorecodes"
    interview_id = Column(Integer, ForeignKey("interviews.id"), primary_key=True)
    score_code_id = Column(Integer, ForeignKey("score_codes.id"), primary_key=True)


class AnalysisRequest(BaseModel):
    question: str
    transcript: str
