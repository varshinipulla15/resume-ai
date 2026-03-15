from services.ats.rule_checker import run_rule_checks
from services.ats.ai_scorer import ai_score_resume


async def run_ats_analysis(resume_text: str, jd_text: str) -> dict:
    # Part 1: Rule-based checks
    rule_result = run_rule_checks(resume_text, jd_text)

    # Part 2: AI scoring
    ai_result = await ai_score_resume(resume_text, jd_text)

    # Part 3: Combined score (50% rule + 50% AI)
    rule_score = rule_result["rule_score"]
    ai_score = ai_result["ai_score"]
    final_score = round((rule_score * 0.5) + (ai_score * 0.5))

    # ATS label
    if final_score >= 80:
        label = "Excellent"
    elif final_score >= 60:
        label = "Good"
    elif final_score >= 40:
        label = "Needs Improvement"
    else:
        label = "Poor"

    return {
        "final_ats_score": final_score,
        "ats_label": label,
        "rule_score": rule_score,
        "ai_score": ai_score,
        "rule_checks": rule_result["checks"],
        "ai_feedback": {
            "keyword_relevance": ai_result["keyword_relevance"],
            "summary_quality": ai_result["summary_quality"],
            "experience_quality": ai_result["experience_quality"],
            "overall_feedback": ai_result["overall_feedback"],
            "top_improvements": ai_result["top_improvements"]
        }
    }