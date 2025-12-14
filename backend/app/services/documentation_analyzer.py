import os
from backend.app.models.analysis_models import DocumentationAnalysis

def find_readme(repo_path: str) -> str | None:
    for file in os.listdir(repo_path):
        if file.lower().startswith("readme"):
            return os.path.join(repo_path, file)
    return None


def read_file_safe(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def detect_sections(text: str) -> dict:
    text_lower = text.lower()

    return {
        "installation": any(k in text_lower for k in ["install", "setup", "requirements"]),
        "usage": any(k in text_lower for k in ["usage", "how to use", "run"]),
        "contributing": "contributing" in text_lower,
        "license": "license" in text_lower
    }


def count_lines(text: str) -> int:
    return len(text.splitlines())


def calculate_doc_ratio(readme_lines: int, loc: int) -> float:
    if loc == 0:
        return 0.0
    return round(readme_lines / loc, 3)


def analyze_documentation(repo_path: str, total_loc: int) -> DocumentationAnalysis:
    readme_path = find_readme(repo_path)

    if not readme_path:
        return DocumentationAnalysis(
            has_readme=False,
            readme_length=0,
            has_installation=False,
            has_usage=False,
            has_contributing=False,
            has_license=False,
            doc_to_code_ratio=0.0
        )

    content = read_file_safe(readme_path)
    sections = detect_sections(content)
    readme_lines = count_lines(content)

    return DocumentationAnalysis(
        has_readme=True,
        readme_length=readme_lines,
        has_installation=sections["installation"],
        has_usage=sections["usage"],
        has_contributing=sections["contributing"],
        has_license=sections["license"],
        doc_to_code_ratio=calculate_doc_ratio(readme_lines, total_loc)
    )
