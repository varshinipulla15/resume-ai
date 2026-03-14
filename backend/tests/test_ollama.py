import httpx

jd_text = """
We are looking for a Senior DevOps Engineer with experience in Docker, 
Kubernetes, Jenkins, AWS, Python scripting, Terraform, Linux administration,
Prometheus monitoring, Grafana dashboards and CI/CD pipeline management.
"""

resume_text = """
DevOps Engineer with 5 years of experience.
Skills: Docker, Kubernetes, AWS, Python, Linux, Jenkins, Git.
Experience with CI/CD pipelines and cloud infrastructure.
"""

prompt = f"""
Extract only the technical skills from this job description.
Return ONLY a comma separated list, no explanation, no extra text.

Job Description:
{jd_text}
"""

response = httpx.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    },
    timeout=60.0
)

raw = response.json()["response"]
jd_skills = [skill.strip().lower() for skill in raw.split(",")]

resume_lower = resume_text.lower()

def is_in_resume(skill: str, resume: str) -> bool:
    # Check full phrase first
    if skill in resume:
        return True
    # Check if ANY key word of the phrase is in resume
    words = skill.split()
    return any(word in resume for word in words if len(word) > 3)

matched = [skill for skill in jd_skills if is_in_resume(skill, resume_lower)]
missing = [skill for skill in jd_skills if not is_in_resume(skill, resume_lower)]

print("JD Skills:", jd_skills)
print("\nMatched:", matched)
print("\nMissing:", missing)