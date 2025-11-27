from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services import scorer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import openai
import json
import re
import os
from dotenv import load_dotenv

app = FastAPI()
router = APIRouter(
    tags=["Submit & Scoring"]
)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
origins = [
    "http://localhost:53947",  # Angular app port
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:53947"],  # Angular frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Answer(BaseModel):
    question: str
    selected_answer: str

class TestSubmission(BaseModel):
    test: dict  
    answers: List[Answer]

class Flag(BaseModel):
    question_index: int
    long_time_taken: bool
    hesitation: bool

@app.post("/submit")
async def submit_test(submission: TestSubmission):
    # call the scoring service
    result = scorer.calculate_score(submission.test, submission.answers)
    return result

@router.post("/analyze-behavior")
async def analyze_behavior(data: dict):
    behavior_data = data.get("behavior_data")

    prompt = f"""
You are a professional hiring behavior analyst AI.

A candidate completed a technical test. Below is the raw telemetry for each question:
{json.dumps(behavior_data, indent=2)}

Your task:
- For **each question**, output:
  - "suspicious": true/false
  - "reason": short text in **2-3 words** like: "too long", "rushed", "many changes", "overthinking", "confident", "competence issue", etc.
- Use the following rules:
  - If time_taken_seconds > estimated_time_seconds * 1.5 → mark as "too long"
  - If time_taken_seconds < estimated_time_seconds * 0.5 → mark as "rushed"
  - If answer_changes >= 3 → mark as "many changes"
  - If both long time + many changes → mark as "overthinking"
  - If time is within normal range and few/no changes → mark as "confident"

Then:
- Provide an overall "summary" and "recommendations".

 Output STRICTLY in this JSON format:
{{
  "summary": "Candidate summary here",
  "recommendations": "Your recommendation text here",
  "questions_analysis": [
    {{
      "question_index": 0,
      "suspicious": true/false,
      "reason": "short reason"
    }},
    ...
  ]
}}

 No other text. No markdown. JSON only. Strictly valid.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a hiring behavior evaluator. Always output valid JSON matching exactly the required structure."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_output = response['choices'][0]['message']['content'].strip()

    # Clean possible ```json``` block
    cleaned_output = re.sub(r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", raw_output, flags=re.MULTILINE).strip()

    try:
        parsed_json = json.loads(cleaned_output)
        return JSONResponse(content=parsed_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GPT response: {e}\nRaw response was: {raw_output}")
