from fastapi import APIRouter, HTTPException
from backend.app.models.request_models import RepoAnalyzeRequest
from backend.app.utils.validators import validate_github_repo_url

router = APIRouter(prefix="/analyze", tags=["Repository Analysis"])

@router.post("/")
def analyze_repository(request: RepoAnalyzeRequest):
    repo_url = request.repo_url

    if not validate_github_repo_url(str(repo_url)):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    return {
        "status": "accepted",
        "repo_url": repo_url,
        "message": "Repository URL validated successfully"
    }
