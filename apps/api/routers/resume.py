from fastapi import APIRouter, UploadFile, File, HTTPException
from services.parsing.profile_extractor import extract_profile_from_text
import fitz  

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text("text"))
        text = "\n".join(text_parts).strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    if not text:
        raise HTTPException(status_code=422, detail="No extractable text found in the PDF.")

    preview = text[:1200]

    return {
        "filename": file.filename,
        "chars": len(text),
        "preview": preview
    }

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_parts = [page.get_text("text") for page in doc]
        text = "\n".join(text_parts).strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    if not text:
        raise HTTPException(status_code=422, detail="No extractable text found in the PDF.")

    profile = extract_profile_from_text(text)
    return {
        "filename": file.filename,
        "profile": profile.model_dump(),
    }
