import os
from collections import defaultdict
from backend.app.models.analysis_models import StructureAnalysis

def analyze_structure(repo_path: str) -> StructureAnalysis:
    file_types = defaultdict(int)
    total_files = 0
    total_dirs = 0
    root_files = []
    max_depth = 0

    for root, dirs, files in os.walk(repo_path):
        depth = root.replace(repo_path, "").count(os.sep)
        max_depth = max(max_depth, depth)
        total_dirs += len(dirs)

        for file in files:
            total_files += 1
            ext = os.path.splitext(file)[1] or "no_ext"
            file_types[ext] += 1

            if root == repo_path:
                root_files.append(file)


    has_readme = any(
        f.lower().startswith("readme") for f in root_files
    )

    has_tests = any(
        d.lower() in ["tests", "test", "__tests__"]
        for d in os.listdir(repo_path)
        if os.path.isdir(os.path.join(repo_path, d))
    )

    has_ci = os.path.exists(
        os.path.join(repo_path, ".github", "workflows")
    )

    return StructureAnalysis(
        total_files=total_files,
        total_directories=total_dirs,
        file_types=dict(file_types),
        has_readme=has_readme,
        has_tests=has_tests,
        has_ci=has_ci,
        root_files=root_files,
        max_depth=max_depth
    )
