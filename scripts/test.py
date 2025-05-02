from app.database import SessionLocal
from app.models import User, Interviews,InterviewFeedback

# Create a database session
db = SessionLocal()

# Now you can query your database
user = db.query(User).filter(User.id == 9).first()
if user:
    print(f"User: {user.email}")
    print(f"Interviews: {len(user.interviews)}")
    for interview in user.interviews:
        print(f"Interview ID: {interview.id}")
        feedback = db.query(InterviewFeedback).filter(User.id == 9).first()
        print(f"Interview feedback: {feedback.clarity_level}")
else:
    print("User not found")

# Don't forget to close the session when you're done
db.close()