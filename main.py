from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pdfplumber
import base64
import spacy

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
        # Access fields from Pydantic model
        pdf_base64 = data.pdf_base64
        job_skills = data.skills

        # Decode the base64 PDF
        if not pdf_base64:
            raise HTTPException(status_code=400, detail="No PDF base64 data provided")

        pdf_data = base64.b64decode(pdf_base64)

        # Extract text using pdfplumber
        text = ""
        with pdfplumber.open(pdf_data) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text:
            return {"text": "", "skills": []}

        # Process text with spaCy
        doc = nlp(text)

        # Extract skills by matching against job_skills
        matched_skills = []
        for token in doc:
            # Check if the token (or phrase) is in the job skills
            if token.text.lower() in [skill.lower() for skill in job_skills]:
                if token.text not in matched_skills:
                    matched_skills.append(token.text)
            # Check for multi-token skills
            for skill in job_skills:
                if skill.lower() in text.lower() and skill not in matched_skills:
                    matched_skills.append(skill)

        return {"text": text, "skills": matched_skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))