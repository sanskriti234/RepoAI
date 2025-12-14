import re

GITHUB_REPO_REGEX = r"^https:\/\/github\.com\/[^\/]+\/[^\/]+\/?$"

def validate_github_repo_url(url: str) -> bool:
    return re.match(GITHUB_REPO_REGEX, url) is not None
