from fastapi import FastAPI, HTTPException  # ✅ Import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import AnalysisRequest
from app.services import get_claude_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_response(request: AnalysisRequest):
    try:
        feedback = await get_claude_feedback(request.question, request.transcript)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # ✅ Now works
