from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    question: str
    transcript: str
