from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pdfplumber
import base64
import spacy
from io import BytesIO
import re

app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define Pydantic model for request body
class ExtractTextRequest(BaseModel):
    pdf_base64: str
    skills: list[str] = []

@app.post("/extract-text")
async def extract_text(data: ExtractTextRequest):
    try:
        pdf_base64 = data.pdf_base64
        job_skills = data.skills

        # Validate PDF data
        if not pdf_base64:
            raise HTTPException(status_code=400, detail="No PDF base64 data provided")

        # Decode base64 PDF
        pdf_data = base64.b64decode(pdf_base64)
        pdf_file = BytesIO(pdf_data)

        # Extract text from PDF
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text:
            return {"text": "", "skills": []}

        # Lowercase the whole text for case-insensitive matching
        lower_text = text.lower()

        # Exact word boundary matching (case-insensitive)
        matched_skills = []
        for skill in job_skills:
            # Build regex pattern with word boundaries
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, lower_text):
                matched_skills.append(skill)

        return {"text": text, "skills": matched_skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
