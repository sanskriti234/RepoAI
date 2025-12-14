import os
from backend.app.models.analysis_models import TestingAnalysis

TEST_DIR_NAMES = ["tests", "test", "__tests__"]

def find_test_directories(repo_path: str) -> list[str]:
    found = []
    for root, dirs, files in os.walk(repo_path):
        for d in dirs:
            if d.lower() in TEST_DIR_NAMES:
                found.append(os.path.join(root, d))
    return found

def count_test_files(test_dirs: list[str]) -> int:
    count = 0
    for d in test_dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().startswith("test") or f.lower().endswith("_test.py"):
                    count += 1
    return count

def detect_test_frameworks(repo_path: str) -> list[str]:
    frameworks = set()

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().lower()
                        if "pytest" in content:
                            frameworks.add("pytest")
                        if "unittest" in content:
                            frameworks.add("unittest")
                except Exception:
                    pass

    return list(frameworks)


def detect_coverage(repo_path: str) -> bool:
    coverage_files = [
        "coverage.xml",
        ".coverage",
        "htmlcov"
    ]

    for root, dirs, files in os.walk(repo_path):
        for item in files + dirs:
            if item in coverage_files:
                return True
    return False


def analyze_testing(repo_path: str) -> TestingAnalysis:
    test_dirs = find_test_directories(repo_path)
    test_files = count_test_files(test_dirs)
    frameworks = detect_test_frameworks(repo_path)
    has_coverage = detect_coverage(repo_path)

    return TestingAnalysis(
        has_tests=len(test_dirs) > 0,
        test_directories=test_dirs,
        test_files_count=test_files,
        test_frameworks=frameworks,
        has_coverage=has_coverage
    )
