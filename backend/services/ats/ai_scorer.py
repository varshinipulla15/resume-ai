import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


async def ai_score_resume(resume_text: str, jd_text: str) -> dict:
    prompt = f"""
You are a strict ATS (Applicant Tracking System) expert. 
Analyze this resume against the job description and return a JSON response only.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Return ONLY this JSON format, no explanation, no extra text:
{{
    "ai_score": <number 0-100>,
    "keyword_relevance": "<feedback on how well keywords match>",
    "summary_quality": "<feedback on the summary section>",
    "experience_quality": "<feedback on experience section>",
    "overall_feedback": "<2-3 sentences of overall feedback>",
    "top_improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"]
}}
"""

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        raw = response.json()["response"]

        # Parse JSON from AI response
        import json
        import re

        # Extract JSON block from response
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            # Fallback if AI doesn't return clean JSON
            result = {
                "ai_score": 50,
                "keyword_relevance": "Could not parse AI response",
                "summary_quality": "Could not parse AI response",
                "experience_quality": "Could not parse AI response",
                "overall_feedback": raw[:200],
                "top_improvements": ["Please try again"]
            }

        return result