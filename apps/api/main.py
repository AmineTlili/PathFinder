from fastapi import FastAPI

app = FastAPI(
    title="PathFinder",
    description="AI-powered Career Intelligence Platform",
    version="0.1.0"
)

@app.get("/")
def health():
    return {"status": "ok", "service": "api"}
