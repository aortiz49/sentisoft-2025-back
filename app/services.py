import asyncio
import time
import re
from concurrent.futures import ThreadPoolExecutor
from anthropic import Anthropic
from app.config import get_claude_api_key

# Synchronous function that calls the Claude API using the official Anthropic client
def call_claude(question: str, transcript: str) -> dict:
    claude_api_key = get_claude_api_key()

    client = Anthropic(api_key=claude_api_key)

    prompt = f"""
    You are a behavioral interview coach.

    Evaluate the following response to the interview question: "{question}"

    Candidate's response:
    {transcript}

    Please provide a score out of 10 of each of the three categories: clarity, structure, and communication style.
    - Feedback on clarity, structure, and communication style.
    - Whether the candidate stayed on topic.
    - Suggested improvements.

    Note: Don't be too harsh while grading but also be fair. The user needs to be able to improve over time!
    """

    start_time = time.time()  # ⏳ Start time

    message = client.messages.create(
        model="claude-3-5-haiku-20241022", 
        max_tokens=1024,
        temperature=0.3,  # Less randomness for consistent scoring
        messages=[{"role": "user", "content": prompt}]
    )

    end_time = time.time()  # ⏳ End time
    print(f"Claude API took {end_time - start_time:.2f} seconds")

    response_text = message.content[0].text  # ✅ Ensure response_text is assigned

    scores, feedback_text = extract_scores(response_text)

    return {
        "clarity": scores["clarity"],
        "structure": scores["structure"],
        "communication": scores["communication"],
        "feedback": feedback_text,  # ✅ Clean feedback without scores
    }

# Async function that wraps the blocking Claude call inside a thread executor
async def get_claude_feedback(question: str, transcript: str) -> dict:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, call_claude, question, transcript)

def extract_scores(response_text: str) -> tuple:
    score_pattern = re.compile(r"Clarity:\s*(\d+)/10|Structure:\s*(\d+)/10|Communication Style:\s*(\d+)/10")
    matches = score_pattern.findall(response_text)

    scores = {
        "clarity": int(matches[0][0]) if matches and matches[0][0] else 0,
        "structure": int(matches[1][1]) if matches and matches[1][1] else 0,
        "communication": int(matches[2][2]) if matches and matches[2][2] else 0,
    }

    # 🔥 Remove the score lines from the feedback text
    feedback_text = re.sub(score_pattern, "", response_text).strip()

    return scores, feedback_text
