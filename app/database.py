# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Strip off +asyncpg if you previously had it
DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "")

# Create a blocking (sync) engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Regular session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
