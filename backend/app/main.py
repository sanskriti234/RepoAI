from fastapi import FastAPI
from backend.app.api.analyze import router as analyze_router

app = FastAPI(
    title="RepoAI",
    description="AI-powered GitHub repository evaluator",
    version="0.1.0"
)

app.include_router(analyze_router)

@app.get("/")
def health_check():
    return {"status": "OK"}
