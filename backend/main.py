from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text_from_docx, extract_text_from_pdf
from services.matcher import get_match_score
#from services.missing_keywords import get_missing_keywords
from services.ai_missing_keywords import analyze_keywords
import os

app = FastAPI(title="AI Resume Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Resume Generator API is running!"}


@app.post("/generate-resume")
async def generate_resume(
    jd: str = Form(...),
    resume: UploadFile = File(...)
):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(file_path, "wb") as f:
        f.write(await resume.read())

    # Extract text based on file type
    if resume.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif resume.filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type. Please upload PDF or DOCX only."}

    # Get match score
    match = get_match_score(extracted_text, jd)
    keywords = await analyze_keywords(extracted_text, jd)
    #keywords = get_missing_keywords(extracted_text, jd)

    return {
        "status": "received",
        "filename": resume.filename,
        "jd_preview": jd[:100],
        "extracted_resume_text": extracted_text,
        "match_score": match["score"],
        "match_label": match["label"],
        "total_jd_keywords": keywords["total_jd_keywords"],
        "matched_keywords": keywords["matched_keywords"],
        "matched_count": keywords["matched_count"],
        "missing_keywords": keywords["missing_keywords"],
        "missing_count": keywords["missing_count"]
    }