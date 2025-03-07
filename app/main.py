from fastapi import FastAPI, HTTPException
from app.models import AnalysisRequest
from app.services import get_claude_feedback

app = FastAPI()

@app.post("/analyze")
async def analyze_response(request: AnalysisRequest):
    try:
        feedback = await get_claude_feedback(request.question, request.transcript)
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
