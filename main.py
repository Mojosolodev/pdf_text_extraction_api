from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

app = FastAPI()

class PDFInput(BaseModel):
    pdf_base64: str

@app.post("/extract-text")
async def extract_text(pdf_input: PDFInput):
    try:
        # Decode base64 PDF
        pdf_data = base64.b64decode(pdf_input.pdf_base64)
        pdf_file = BytesIO(pdf_data)
        
        # Extract text using pdfminer.six
        output_string = BytesIO()
        extract_text_to_fp(pdf_file, output_string, laparams=LAParams())
        text = output_string.getvalue().decode('utf-8')
        
        if not text.strip():
            return {"error": "No text extracted from PDF"}
            
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")