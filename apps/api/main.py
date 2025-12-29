from fastapi import FastAPI
from routers.resume import router as resume_router
from routers.rag import router as rag_router
from dotenv import load_dotenv
from routers.assistant import router as assistant_router
from routers.job import router as job_router


load_dotenv()

app = FastAPI(
    title="PathFinder",
    description="AI-powered Career Intelligence Platform",
    version="0.1.0",
)


app.include_router(resume_router)
app.include_router(rag_router)
app.include_router(assistant_router)
app.include_router(job_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "api"}