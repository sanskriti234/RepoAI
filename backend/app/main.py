from fastapi import FastAPI

app = FastAPI(
    title="RepoAI",
    description="AI-powered GitHub repository evaluator",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {
        "status": "OK",
        "message": "RepoAI backend running"
    }
