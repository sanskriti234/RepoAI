from urllib.parse import urlparse
import requests
from backend.app.config import GITHUB_API_BASE, GITHUB_TOKEN
import os
from git import Repo

BASE_CLONE_DIR = "data/cloned_repos"


import tempfile

import shutil
import subprocess

def clone_repository(repo_url: str, repo_name: str) -> str:
    base_dir = tempfile.mkdtemp(prefix="repoai_")
    repo_path = os.path.join(base_dir, repo_name)

    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, repo_path],
        check=True
    )

    return repo_path



def extract_owner_repo(repo_url: str) -> tuple[str, str]:
    """
    Extracts owner and repository name from GitHub URL
    """
    path = urlparse(repo_url).path.strip("/")
    owner, repo = path.split("/")[:2]
    return owner, repo


HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def fetch_repo_metadata(owner: str, repo: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)

    print("GitHub API STATUS:", response.status_code)
    print("GitHub API RESPONSE:", response.text)

    if response.status_code != 200:
        raise Exception("Failed to fetch repository metadata")

    return response.json()


def fetch_commit_stats(owner: str, repo: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception("Failed to fetch commits")

    commits = response.json()
    return {
        "total_commits_sampled": len(commits),
        "latest_commit_date": commits[0]["commit"]["author"]["date"]
        if commits else None
    }


def fetch_languages(owner: str, repo: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception("Failed to fetch languages")

    return response.json()
