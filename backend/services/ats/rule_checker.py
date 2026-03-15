import re
from collections import Counter

# Required resume sections
REQUIRED_SECTIONS = ["experience", "education", "skills", "summary"]

# Action verbs that ATS systems love
ACTION_VERBS = [
    "led", "built", "managed", "developed", "designed", "implemented",
    "created", "improved", "increased", "reduced", "delivered", "deployed",
    "automated", "optimized", "architected", "configured", "maintained",
    "monitored", "migrated", "integrated", "collaborated", "coordinated"
]

# Contact info patterns
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'[\+]?[\d\s\-\(\)]{7,15}'

# Personal pronouns
PERSONAL_PRONOUNS = [
    "i ", "i'm", "i've", "i'd", "i'll",
    "me ", "my ", "mine", "myself",
    "we ", "we're", "our ", "ours"
]

# Generic weak phrases
GENERIC_PHRASES = [
    "team player", "hard worker", "hardworking", "go-getter",
    "self-starter", "detail oriented", "detail-oriented",
    "results driven", "results-driven", "highly motivated",
    "passionate about", "think outside the box",
    "strong communication skills", "excellent communication",
    "good communication", "people person", "fast learner",
    "quick learner", "dynamic", "synergy", "leverage",
    "proactive", "go above and beyond", "wear many hats"
]

# Buzzwords to avoid
BUZZWORDS = [
    "synergy", "leverage", "utilize", "utilized", "utilizing",
    "bandwidth", "ecosystem", "holistic", "paradigm", "scalable",
    "innovative", "cutting-edge", "best-of-breed", "thought leader",
    "disruptive", "game-changer", "move the needle", "deep dive",
    "circle back", "boil the ocean", "drinking the kool-aid",
    "value-add", "low-hanging fruit", "take offline", "pivot"
]

# Passive voice indicators
PASSIVE_INDICATORS = [
    r'\bwas\s+\w+ed\b',
    r'\bwere\s+\w+ed\b',
    r'\bbeen\s+\w+ed\b',
    r'\bis\s+\w+ed\b',
    r'\bare\s+\w+ed\b',
    r'\bwas\s+\w+en\b',
    r'\bwere\s+\w+en\b',
]

# Quantity patterns for achievements
QUANTITY_PATTERNS = [
    r'\d+\s*%',
    r'\d+\s*x\b',
    r'\$\s*\d+',
    r'\d+\s*(servers?|systems?|applications?|services?|teams?|members?|clients?|users?|projects?)',
    r'(increased|decreased|reduced|improved|grew|saved|cut)\s.*\d+',
    r'\d+\s*(years?|months?|weeks?)',
]

# Date formats for consistency check
DATE_PATTERNS = {
    "mm/yyyy": r'\b(0?[1-9]|1[0-2])\/\d{4}\b',
    "month_yyyy": r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
    "mon_yyyy": r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4}\b',
    "yyyy": r'\b(19|20)\d{2}\b',
}

# Red flag content
REFERENCES_PHRASES = [
    "references available upon request",
    "references available",
    "references on request",
    "references furnished upon request"
]

AGE_DOB_PATTERNS = [
    r'\b(date of birth|dob|d\.o\.b|age\s*:)\b',
    r'\bborn\s+in\s+\d{4}\b',
    r'\bage\s*:\s*\d+\b',
]

# Common job titles for title matching
TITLE_KEYWORDS = [
    "engineer", "developer", "manager", "analyst", "architect",
    "designer", "consultant", "specialist", "coordinator", "director",
    "lead", "senior", "junior", "devops", "frontend", "backend",
    "fullstack", "data", "cloud", "security", "network", "software"
]


# ── Individual Check Functions ─────────────────────────────────

def check_sections(text: str) -> dict:
    text_lower = text.lower()
    found = [s for s in REQUIRED_SECTIONS if s in text_lower]
    missing = [s for s in REQUIRED_SECTIONS if s not in text_lower]
    score = (len(found) / len(REQUIRED_SECTIONS)) * 100
    return {
        "score": round(score),
        "found": found,
        "missing": missing,
        "feedback": f"Found {len(found)}/{len(REQUIRED_SECTIONS)} required sections"
            + (f" — add: {missing}" if missing else " ✓")
    }


def check_contact_info(text: str) -> dict:
    has_email = bool(re.search(EMAIL_PATTERN, text))
    has_phone = bool(re.search(PHONE_PATTERN, text))
    has_linkedin = "linkedin" in text.lower()
    found = []
    if has_email: found.append("email")
    if has_phone: found.append("phone")
    if has_linkedin: found.append("linkedin")
    score = (len(found) / 3) * 100
    return {
        "score": round(score),
        "found": found,
        "feedback": f"Found {len(found)}/3 contact details"
            + (" ✓" if len(found) == 3 else f" — missing: {set(['email','phone','linkedin']) - set(found)}")
    }


def check_action_verbs(text: str) -> dict:
    text_lower = text.lower()
    found = [v for v in ACTION_VERBS if v in text_lower]
    score = min(100, (len(found) / 5) * 100)
    return {
        "score": round(score),
        "found": found,
        "feedback": f"Found {len(found)} action verbs"
            + (" ✓" if len(found) >= 5 else " — aim for 5+")
    }


def check_length(text: str) -> dict:
    word_count = len(text.split())
    char_count = len(text.strip())
    # Estimate pages (avg 450 words per page)
    estimated_pages = round(word_count / 450, 1)

    issues = []

    # Word count check
    if word_count < 300:
        word_score = 40
        issues.append(f"too short ({word_count} words, aim for 300-800)")
    elif word_count > 1000:
        word_score = 50
        issues.append(f"too long ({word_count} words, aim for 300-800)")
    elif 300 <= word_count <= 800:
        word_score = 100
    else:
        word_score = 75
        issues.append(f"slightly long ({word_count} words)")

    # Page estimate check
    if estimated_pages < 0.5:
        page_score = 30
        issues.append(f"less than half a page ({estimated_pages} pages)")
    elif estimated_pages > 2.5:
        page_score = 40
        issues.append(f"more than 2 pages ({estimated_pages} pages) — keep to 1-2 pages")
    elif 1.0 <= estimated_pages <= 2.0:
        page_score = 100
    else:
        page_score = 75

    # Character count check
    if char_count < 1000:
        char_score = 40
        issues.append(f"very little content ({char_count} characters)")
    elif char_count > 6000:
        char_score = 60
        issues.append(f"too much content ({char_count} characters)")
    else:
        char_score = 100

    # Combined score
    score = round((word_score * 0.5) + (page_score * 0.3) + (char_score * 0.2))

    feedback = (
        f"Good length — {word_count} words, ~{estimated_pages} pages ✓"
        if not issues else
        f"Length issues: {', '.join(issues)}"
    )

    return {
        "score": score,
        "word_count": word_count,
        "char_count": char_count,
        "estimated_pages": estimated_pages,
        "feedback": feedback
    }


def check_quantified_achievements(text: str) -> dict:
    found = []
    for pattern in QUANTITY_PATTERNS:
        matches = re.findall(pattern, text.lower())
        found.extend(matches)
    found = list(set(found))
    score = min(100, (len(found) / 3) * 100)
    if len(found) == 0:
        feedback = "No quantified achievements — add numbers like 'reduced costs by 30%'"
    elif len(found) < 3:
        feedback = f"Found {len(found)} quantified achievement(s) — try to add more"
    else:
        feedback = f"Great! Found {len(found)} quantified achievements ✓"
    return {"score": round(score), "found": found, "count": len(found), "feedback": feedback}


def check_personal_pronouns(text: str) -> dict:
    text_lower = text.lower()
    found = [p for p in PERSONAL_PRONOUNS if p in text_lower]
    score = max(0, 100 - (len(found) * 20))
    feedback = "No personal pronouns found ✓" if not found else \
        f"Found pronouns: {found} — remove for better ATS score"
    return {"score": round(score), "found": found, "feedback": feedback}


def check_generic_phrases(text: str) -> dict:
    text_lower = text.lower()
    found = [p for p in GENERIC_PHRASES if p in text_lower]
    score = max(0, 100 - (len(found) * 15))
    feedback = "No generic phrases found ✓" if not found else \
        f"Found generic phrases: {found} — replace with specific achievements"
    return {"score": round(score), "found": found, "feedback": feedback}


def check_buzzwords(text: str) -> dict:
    text_lower = text.lower()
    found = [b for b in BUZZWORDS if b in text_lower]
    score = max(0, 100 - (len(found) * 15))
    feedback = "No buzzwords found ✓" if not found else \
        f"Found buzzwords: {found} — replace with concrete descriptions"
    return {"score": round(score), "found": found, "feedback": feedback}


def check_passive_voice(text: str) -> dict:
    text_lower = text.lower()
    found = []
    for pattern in PASSIVE_INDICATORS:
        matches = re.findall(pattern, text_lower)
        found.extend(matches)
    found = list(set(found))
    score = max(0, 100 - (len(found) * 10))
    feedback = "No passive voice found ✓" if not found else \
        f"Found {len(found)} passive voice instance(s): {found} — use active voice"
    return {"score": round(score), "found": found, "feedback": feedback}


def check_repetitive_words(text: str) -> dict:
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    word_counts = Counter(words)
    # Filter stop words
    stop = {"with", "that", "this", "from", "have", "been", "will",
            "your", "they", "their", "were", "also", "more", "into"}
    repeated = {w: c for w, c in word_counts.items()
                if c >= 4 and w not in stop}
    score = max(0, 100 - (len(repeated) * 10))
    feedback = "No repetitive words found ✓" if not repeated else \
        f"Overused words: {list(repeated.keys())} — vary your vocabulary"
    return {"score": round(score), "repeated": repeated, "feedback": feedback}


def check_date_consistency(text: str) -> dict:
    formats_found = {}
    for fmt, pattern in DATE_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            formats_found[fmt] = len(matches)

    if len(formats_found) == 0:
        score = 50
        feedback = "No dates found — add employment dates"
    elif len(formats_found) == 1:
        score = 100
        feedback = f"Dates are consistent ({list(formats_found.keys())[0]} format) ✓"
    else:
        score = 50
        feedback = f"Mixed date formats found: {list(formats_found.keys())} — use one consistent format"

    return {"score": score, "formats_found": formats_found, "feedback": feedback}


def check_references_line(text: str) -> dict:
    text_lower = text.lower()
    found = [p for p in REFERENCES_PHRASES if p in text_lower]
    score = 0 if found else 100
    feedback = f"Remove '{found[0]}' — wastes valuable space" if found else \
        "No references line found ✓"
    return {"score": score, "found": found, "feedback": feedback}


def check_age_dob(text: str) -> dict:
    text_lower = text.lower()
    found = []
    for pattern in AGE_DOB_PATTERNS:
        matches = re.findall(pattern, text_lower)
        found.extend(matches)
    score = 0 if found else 100
    feedback = "Age/DOB found — remove personal info to avoid bias filtering" \
        if found else "No age/DOB found ✓"
    return {"score": score, "found": found, "feedback": feedback}


def check_title_match(resume_text: str, jd_text: str) -> dict:
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    jd_titles = [t for t in TITLE_KEYWORDS if t in jd_lower]
    matched = [t for t in jd_titles if t in resume_lower]
    score = round((len(matched) / len(jd_titles)) * 100) if jd_titles else 100
    feedback = f"Title keywords matched: {matched} ✓" if matched else \
        f"No title keywords matched — consider adding: {jd_titles[:3]}"
    return {"score": score, "matched": matched, "feedback": feedback}


def check_years_of_experience(resume_text: str, jd_text: str) -> dict:
    # Extract years required from JD
    jd_years = re.findall(r'(\d+)\+?\s*years?\s*(of\s*)?(experience)?', jd_text.lower())
    # Extract years mentioned in resume
    resume_years = re.findall(r'(\d+)\+?\s*years?\s*(of\s*)?(experience)?', resume_text.lower())

    if not jd_years:
        return {"score": 100, "feedback": "No specific years of experience required in JD ✓"}

    required = max([int(y[0]) for y in jd_years])
    has_years = max([int(y[0]) for y in resume_years]) if resume_years else 0

    if has_years >= required:
        score = 100
        feedback = f"Experience matches — has {has_years} years, JD requires {required} ✓"
    else:
        score = 50
        feedback = f"Experience gap — has {has_years} years, JD requires {required}"

    return {"score": score, "required": required, "found": has_years, "feedback": feedback}


# ── Main Runner ────────────────────────────────────────────────

def run_rule_checks(resume_text: str, jd_text: str = "") -> dict:
    sections = check_sections(resume_text)
    contact = check_contact_info(resume_text)
    verbs = check_action_verbs(resume_text)
    length = check_length(resume_text)
    achievements = check_quantified_achievements(resume_text)
    pronouns = check_personal_pronouns(resume_text)
    generic = check_generic_phrases(resume_text)
    buzzwords = check_buzzwords(resume_text)
    passive = check_passive_voice(resume_text)
    repetitive = check_repetitive_words(resume_text)
    dates = check_date_consistency(resume_text)
    references = check_references_line(resume_text)
    age_dob = check_age_dob(resume_text)
    title = check_title_match(resume_text, jd_text) if jd_text else None
    experience = check_years_of_experience(resume_text, jd_text) if jd_text else None

    # Build checks dict
    checks = {
        "sections": sections,
        "contact_info": contact,
        "action_verbs": verbs,
        "length": length,
        "quantified_achievements": achievements,
        "personal_pronouns": pronouns,
        "generic_phrases": generic,
        "buzzwords": buzzwords,
        "passive_voice": passive,
        "repetitive_words": repetitive,
        "date_consistency": dates,
        "references_line": references,
        "age_dob": age_dob,
    }
    if title: checks["title_match"] = title
    if experience: checks["years_of_experience"] = experience

    # Weighted score
    overall = round((
        sections["score"] * 0.15 +
        contact["score"] * 0.10 +
        verbs["score"] * 0.10 +
        length["score"] * 0.05 +
        achievements["score"] * 0.15 +
        pronouns["score"] * 0.08 +
        generic["score"] * 0.08 +
        buzzwords["score"] * 0.07 +
        passive["score"] * 0.07 +
        repetitive["score"] * 0.05 +
        dates["score"] * 0.05 +
        references["score"] * 0.03 +
        age_dob["score"] * 0.02
    ))

    return {
        "rule_score": overall,
        "checks": checks
    }