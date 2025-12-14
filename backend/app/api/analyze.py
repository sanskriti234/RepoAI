from fastapi import APIRouter, HTTPException
from backend.app.models.request_models import RepoAnalyzeRequest
from backend.app.utils.validators import validate_github_repo_url
from backend.app.services.structure_analyzer import analyze_structure
from backend.app.services.github_service import (
    extract_owner_repo,
    fetch_repo_metadata,
    fetch_commit_stats,
    fetch_languages,
    clone_repository
)
from backend.app.services.code_quality_analyzer import analyze_code_quality
from backend.app.services.documentation_analyzer import analyze_documentation
from backend.app.services.testing_analyzer import analyze_testing


router = APIRouter(prefix="/analyze", tags=["Repository Analysis"])


@router.post("/")
def analyze_repository(request: RepoAnalyzeRequest):
    repo_url = str(request.repo_url)

    # 1. Validate GitHub URL
    if not validate_github_repo_url(repo_url):
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    # 2. Extract owner and repo
    owner, repo = extract_owner_repo(repo_url)

    # 3. Fetch repository metadata
    try:
        metadata = fetch_repo_metadata(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4. Clone repository (IMPORTANT: before analysis)
    try:
        local_repo_path = clone_repository(repo_url, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Repository clone failed: {e}")

    # 5. Analyze repository structure
    structure = analyze_structure(local_repo_path)
    code_quality = analyze_code_quality(local_repo_path)
    documentation = analyze_documentation(
        local_repo_path,
        code_quality.total_lines_of_code
    )
    testing = analyze_testing(local_repo_path)

    # 6. Fetch commits and languages
    commits = fetch_commit_stats(owner, repo)
    languages = fetch_languages(owner, repo)

    # 7. Return structured response
    return {
        "status": "testing_analyzed",
        "repository": f"{owner}/{repo}",
        "metadata": {
            "stars": metadata.get("stargazers_count"),
            "forks": metadata.get("forks_count"),
            "open_issues": metadata.get("open_issues_count")
        },
        "commits": commits,
        "languages": languages,
        "structure": structure.dict(),
        "code_quality": code_quality.dict(),
        "documentation": documentation.dict(),
        "testing": testing.dict()
    }
