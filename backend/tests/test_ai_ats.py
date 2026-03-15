import asyncio
import sys
sys.path.append(".")
from services.ats.ai_scorer import ai_score_resume

resume_text = """
John Doe
john@email.com | +1 234 567 8900 | linkedin.com/in/johndoe

Summary
DevOps Engineer with 5 years of experience building CI/CD pipelines.

Skills
Docker, Kubernetes, AWS, Python, Linux, Jenkins

Experience
Led migration of infrastructure to AWS, reducing costs by 40%.
Built CI/CD pipelines using Jenkins, improving deployment speed by 3x.
Managed 5 servers and deployed containerized applications using Docker.

Education
Bachelor of Computer Science, May 2015
"""

jd_text = """
We are looking for a Senior DevOps Engineer with 5+ years of experience
in Docker, Kubernetes, AWS, Terraform and CI/CD pipeline management.
"""

async def main():
    result = await ai_score_resume(resume_text, jd_text)
    print(f"\nAI Score: {result['ai_score']}/100")
    print(f"\nKeyword Relevance: {result['keyword_relevance']}")
    print(f"\nSummary Quality: {result['summary_quality']}")
    print(f"\nExperience Quality: {result['experience_quality']}")
    print(f"\nOverall Feedback: {result['overall_feedback']}")
    print(f"\nTop Improvements:")
    for i, tip in enumerate(result['top_improvements'], 1):
        print(f"  {i}. {tip}")

asyncio.run(main())