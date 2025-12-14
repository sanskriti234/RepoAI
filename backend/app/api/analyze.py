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
from backend.app.services.git_practices_analyzer import analyze_git_practices

from backend.app.core.scoring_engine import calculate_final_score
from backend.app.services.ai_summary_service import generate_repo_summary
from backend.app.services.ai_roadmap_service import generate_dynamic_roadmap
from backend.app.services.ai_repo_explainer import generate_repo_explanation
from backend.app.services.documentation_analyzer import get_readme_content
import os

router = APIRouter(prefix="/analyze", tags=["Repository Analysis"])


@router.post("/")
def analyze_repository(request: RepoAnalyzeRequest):
    repo_url = str(request.repo_url)

    # 1. Validate URL
    if not validate_github_repo_url(repo_url):
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    # 2. Extract owner/repo
    owner, repo = extract_owner_repo(repo_url)

    # 3. Metadata
    try:
        metadata = fetch_repo_metadata(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4. Clone
    try:
        local_repo_path = clone_repository(repo_url, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Repository clone failed: {e}")

    # 5. Analysis
    structure = analyze_structure(local_repo_path)
    code_quality = analyze_code_quality(local_repo_path)
    documentation = analyze_documentation(
        local_repo_path,
        code_quality.total_lines_of_code
    )
    readme_text = get_readme_content(local_repo_path)

    repo_explanation = generate_repo_explanation(
        repo,
        readme_text
    )

    testing = analyze_testing(local_repo_path)
    git_practices = analyze_git_practices(owner, repo)

    # 6. Scoring
    score = calculate_final_score(
        structure,
        code_quality,
        documentation,
        testing,
        git_practices
    )

    # 7. Summary (safe – fallback inside)
    summary = generate_repo_summary(
        repo,
        score,
        structure,
        code_quality,
        documentation,
        testing,
        git_practices
    )

    # 8. Roadmap (FIXED)
    roadmap = generate_dynamic_roadmap(
    repo,
    score,
    structure,
    code_quality,
    documentation,
    testing,
    git_practices
)


    # 9. Extra metadata
    commits = fetch_commit_stats(owner, repo)
    languages = fetch_languages(owner, repo)

    ai_used = "GROQ_API_KEY" in os.environ

    return {
    "status": "completed",
    "repository": f"{owner}/{repo}",
    "score": score.dict(),

    "project_overview": repo_explanation,   # ✅ NEW

    "summary": summary,
    "roadmap": roadmap.dict(),

    "analysis": {
        "structure": structure.dict(),
        "code_quality": code_quality.dict(),
        "project_overview": repo_explanation,
        "documentation": documentation.dict(),
        "testing": testing.dict(),
        "git_practices": git_practices.dict()
    }
}

    
