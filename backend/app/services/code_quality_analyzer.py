import os
import subprocess
from backend.app.models.analysis_models import CodeQualityAnalysis


def collect_python_files(repo_path: str) -> list[str]:
    py_files = []
    for root, dirs, files in os.walk(repo_path):
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def count_loc(files: list[str]) -> int:
    total = 0
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file:
                total += sum(1 for _ in file)
        except Exception:
            pass
    return total


import re

def run_radon(repo_path: str) -> tuple[float, list]:
    result = subprocess.run(
        ["radon", "cc", repo_path, "-a", "-s"],
        capture_output=True,
        text=True
    )

    avg_complexity = 0.0
    high_risk = []

    for line in result.stdout.splitlines():

        # Extract numeric complexity safely
        if "Average complexity" in line:
            match = re.search(r"\(([\d\.]+)\)", line)
            if match:
                avg_complexity = float(match.group(1))

        # Detect risky files (D, E, F)
        if any(f"({grade})" in line for grade in ["D", "E", "F"]):
            high_risk.append(line)

    return avg_complexity, high_risk


def run_pylint(files: list[str]) -> float | None:
    if not files:
        return None

    result = subprocess.run(
        ["pylint", *files, "--score=y"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "Your code has been rated at" in line:
            return float(line.split("/")[0].split()[-1])

    return None


def analyze_code_quality(repo_path: str) -> CodeQualityAnalysis:
    py_files = collect_python_files(repo_path)
    loc = count_loc(py_files)
    avg_complexity, risky = run_radon(repo_path)
    pylint_score = run_pylint(py_files)

    return CodeQualityAnalysis(
        total_code_files=len(py_files),
        total_lines_of_code=loc,
        average_complexity=avg_complexity,
        high_complexity_files=risky,
        pylint_score=pylint_score
    )
