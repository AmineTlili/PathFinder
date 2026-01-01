from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import requests
import os
import json
import re

from services.llm.ollama_client import ollama_generate

router = APIRouter(prefix="/apply", tags=["Apply"])

class ApplyKitRequest(BaseModel):
    job_id: str
    top_k_resume: int = Field(default=6, ge=1, le=12)
    tone: str = Field(default="professional")

@router.post("/kit")
def apply_kit(req: ApplyKitRequest):
    # Call your own API /job/match to reuse existing retrieval logic
    api_base = os.getenv("API_BASE", "http://127.0.0.1:8000")

    try:
        r = requests.post(
            f"{api_base}/job/match",
            json={"job_id": req.job_id, "top_k_resume": req.top_k_resume},
            timeout=300
        )
        r.raise_for_status()
        match_payload = r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to call /job/match: {str(e)}")

    job_ctx = match_payload.get("job_context_used", "")
    resume_ctx = match_payload.get("resume_context_used", [])

    if not job_ctx or not resume_ctx:
        raise HTTPException(status_code=400, detail="Missing context. Ensure job is uploaded and resume is indexed.")

    prompt = f"""
You are a senior recruiter + career coach.

TASK:
Generate an "Apply Kit" tailored to this job, using ONLY the resume evidence provided.
If something is missing, DO NOT invent it. Propose how to close the gap.

Return STRICT JSON ONLY with this exact schema:

{{
  "cv_bullets": ["..."],
  "why_me_summary": "string",
  "cover_letter_short": "string",
  "linkedin_message": "string",
  "interview_questions": [{{"question":"...", "suggested_answer":"..."}}],
  "upskilling_plan_7_days": ["..."],
  "evidence_used": ["RESUME_CHUNK 1", "RESUME_CHUNK 2"]
}}

TONE: {req.tone}

JOB CONTEXT:
{job_ctx}

RESUME CONTEXT:
{chr(10).join(resume_ctx)}
""".strip()

    llm_out = ollama_generate(prompt)

    match = re.search(r"\{.*\}", llm_out, re.DOTALL)
    if not match:
        return {"job_id": req.job_id, "raw_llm": llm_out, "error": "LLM did not return JSON."}

    try:
        data = json.loads(match.group(0))
    except Exception:
        return {"job_id": req.job_id, "raw_llm": llm_out, "error": "Failed to parse JSON."}

    return {
        "job_id": req.job_id,
        "result": data,
        "job_context_used": job_ctx,
        "resume_context_used": resume_ctx
    }
