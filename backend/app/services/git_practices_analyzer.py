import requests
from datetime import datetime, timezone
from backend.app.config import GITHUB_API_BASE, GITHUB_TOKEN
from backend.app.models.analysis_models import GitPracticesAnalysis


HEADERS = {
    "Accept": "application/vnd.github+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def fetch_commits(owner: str, repo: str) -> list:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return []

    return response.json()


def calculate_recent_activity(commits: list) -> int | None:
    if not commits:
        return None

    latest_date_str = commits[0]["commit"]["author"]["date"]
    latest_date = datetime.fromisoformat(latest_date_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    return (now - latest_date).days


def evaluate_commit_messages(commits: list) -> str:
    if not commits:
        return "poor"

    bad_keywords = ["update", "fix", "final", "changes", "test"]
    meaningful = 0

    for c in commits[:10]:  # sample last 10
        msg = c["commit"]["message"].lower()
        if len(msg.split()) > 3 and not any(b in msg for b in bad_keywords):
            meaningful += 1

    if meaningful >= 7:
        return "good"
    elif meaningful >= 4:
        return "average"
    return "poor"


def has_multiple_branches(owner: str, repo: str) -> bool:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/branches"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return False

    branches = response.json()
    return len(branches) > 1


def has_pull_requests(owner: str, repo: str) -> bool:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls?state=all"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return False

    prs = response.json()
    return len(prs) > 0


def analyze_git_practices(owner: str, repo: str) -> GitPracticesAnalysis:
    commits = fetch_commits(owner, repo)

    recent_days = calculate_recent_activity(commits)
    commit_quality = evaluate_commit_messages(commits)

    branches = has_multiple_branches(owner, repo)
    prs = has_pull_requests(owner, repo)

    is_active = recent_days is not None and recent_days <= 180

    return GitPracticesAnalysis(
        total_commits=len(commits),
        recent_activity_days=recent_days,
        commit_message_quality=commit_quality,
        has_multiple_branches=branches,
        has_pull_requests=prs,
        is_actively_maintained=is_active
    )
