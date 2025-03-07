import asyncio
from concurrent.futures import ThreadPoolExecutor
from anthropic import Anthropic
from app.config import get_claude_api_key

# Synchronous function that calls the Claude API using the official Anthropic client
def call_claude(question: str, transcript: str) -> str:
    claude_api_key = get_claude_api_key()

    client = Anthropic(api_key=claude_api_key)

    prompt = f"""
    You are a behavioral interview coach.

    Evaluate the following response to the interview question: "{question}"

    Candidate's response:
    {transcript}

    Please provide:
    - Feedback on clarity, structure, and communication style.
    - Whether the candidate stayed on topic.
    - Suggested improvements.
    """

    message = client.messages.create(
        model="claude-3-5-haiku-20241022", 
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    # Combine all parts into a single string (Claude responses can have multiple parts)
    return " ".join(part.text for part in message.content)

# Async function that wraps the blocking Claude call inside a thread executor
async def get_claude_feedback(question: str, transcript: str) -> str:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, call_claude, question, transcript)
