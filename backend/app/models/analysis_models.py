from pydantic import BaseModel
from typing import Dict, List

class StructureAnalysis(BaseModel):
    total_files: int
    total_directories: int
    file_types: Dict[str, int]
    has_readme: bool
    has_tests: bool
    has_ci: bool
    root_files: List[str]
    max_depth: int


class CodeQualityAnalysis(BaseModel):
    total_code_files: int
    total_lines_of_code: int
    average_complexity: float
    high_complexity_files: list
    pylint_score: float | None


class DocumentationAnalysis(BaseModel):
    has_readme: bool
    readme_length: int
    has_installation: bool
    has_usage: bool
    has_contributing: bool
    has_license: bool
    doc_to_code_ratio: float


class TestingAnalysis(BaseModel):
    has_tests: bool
    test_directories: list
    test_files_count: int
    test_frameworks: list
    has_coverage: bool


class GitPracticesAnalysis(BaseModel):
    total_commits: int
    recent_activity_days: int | None
    commit_message_quality: str
    has_multiple_branches: bool
    has_pull_requests: bool
    is_actively_maintained: bool
