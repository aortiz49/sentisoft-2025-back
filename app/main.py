from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import AnalysisRequest
from app.services import get_claude_feedback
import logging

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

if os.getenv("ENVIRONMENT") == "production": # Verificar si el ambiente es producción o no
    allowed_origin = ["https://sentisoft-2025-front.vercel.app/"] # Hay que poner el dominio real

else:
    allowed_origin = ["http://localhost:5173", "*"] 



app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origin,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_response(request: AnalysisRequest):
    try:
        logger.info(f"Received request for analysis: {request.question}")

        feedback = await get_claude_feedback(request.question, request.transcript)

        logger.info(f"Generated feedback: {feedback}")

        return {"feedback": feedback}

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error. Check logs.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
