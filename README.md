# sentisoft-2025-back
# Behavioral Interview Backend

This is a FastAPI backend to analyze behavioral interview responses using Claude.

## Setup

1. Clone the repo.
2. Create `.env` with:
    ```
    CLAUDE_API_KEY=your-actual-claude-api-key
    ```
3. Install dependencies:
    ```
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
4. Run:
    ```
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

## API

### POST /analyze

**Request Body**

```json
{
    "question": "How do you handle team conflict?",
    "transcript": "I usually talk to both sides and make sure everyone is heard."
}
