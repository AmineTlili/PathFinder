from fastapi import FastAPI
from routers.resume import router as resume_router

app = FastAPI(
    title="PathFinder",
    description="AI-powered Career Intelligence Platform",
    version="0.1.0",
)

app.include_router(resume_router)

@app.get("/")
def health():
    return {"status": "ok", "service": "api"}
