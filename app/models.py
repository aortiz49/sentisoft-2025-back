from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(BaseEntity):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    b2c = Column(Boolean, nullable=False, default=False)
    interview_count = Column(Integer, nullable=False, default=0)
    linkedin_url = Column(String, nullable=True)


class AnalysisRequest(BaseModel):
    question: str
    transcript: str
