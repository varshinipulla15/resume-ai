import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


async def extract_jd_skills(jd_text: str) -> list:
    prompt = f"""
Extract only the technical skills from this job description.
Return ONLY a comma separated list, no explanation, no extra text.

Job Description:
{jd_text}
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
        # Remove any intro text before the actual list
        if "\n\n" in raw:
         raw = raw.split("\n\n")[-1]
        skills = [skill.strip().lower() for skill in raw.split(",")]
        # Remove any skills that are too long (likely intro sentences)
        skills = [s for s in skills if len(s) < 50]
        return skills


def is_in_resume(skill: str, resume: str) -> bool:
    if skill in resume:
        return True
    words = skill.split()
    return any(word in resume for word in words if len(word) > 3)


async def analyze_keywords(resume_text: str, jd_text: str) -> dict:
    resume_lower = resume_text.lower()
    jd_skills = await extract_jd_skills(jd_text)

    matched = [skill for skill in jd_skills if is_in_resume(skill, resume_lower)]
    missing = [skill for skill in jd_skills if not is_in_resume(skill, resume_lower)]

    return {
        "total_jd_keywords": len(jd_skills),
        "matched_keywords": matched,
        "matched_count": len(matched),
        "missing_keywords": missing,
        "missing_count": len(missing)
    }