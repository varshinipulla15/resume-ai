import asyncio
import sys
sys.path.append(".")
from services.ats.ats_engine import run_ats_analysis

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
    result = await run_ats_analysis(resume_text, jd_text)

    print(f"\n{'='*50}")
    print(f"FINAL ATS SCORE: {result['final_ats_score']}/100 — {result['ats_label']}")
    print(f"{'='*50}")
    print(f"Rule Score:  {result['rule_score']}/100")
    print(f"AI Score:    {result['ai_score']}/100")
    print(f"\n── Rule Checks ──")
    for check, data in result["rule_checks"].items():
        print(f"[{data['score']:3}/100] {check}: {data['feedback']}")
    print(f"\n── AI Feedback ──")
    print(f"Keywords:   {result['ai_feedback']['keyword_relevance']}")
    print(f"Summary:    {result['ai_feedback']['summary_quality']}")
    print(f"Experience: {result['ai_feedback']['experience_quality']}")
    print(f"Overall:    {result['ai_feedback']['overall_feedback']}")
    print(f"\nTop Improvements:")
    for i, tip in enumerate(result['ai_feedback']['top_improvements'], 1):
        print(f"  {i}. {tip}")

asyncio.run(main())