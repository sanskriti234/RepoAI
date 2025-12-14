from backend.app.models.analysis_models import (
    ImprovementRoadmap,
    RoadmapItem
)


def generate_roadmap(structure, code, doc, testing, git, score) -> ImprovementRoadmap:
    items = []
    priority = 1

    # ---- TESTING (HIGHEST IMPACT) ----
    if not testing.has_tests:
        items.append(RoadmapItem(
            priority=priority,
            category="Testing",
            action="Introduce a test suite using pytest and add unit tests for core functionality.",
            expected_impact="Improves reliability and confidence in code changes."
        ))
        priority += 1

    elif testing.test_files_count < 5:
        items.append(RoadmapItem(
            priority=priority,
            category="Testing",
            action="Expand the existing test suite to cover more edge cases and modules.",
            expected_impact="Improves test coverage and reduces regression risk."
        ))
        priority += 1

    if testing.has_tests and not testing.has_coverage:
        items.append(RoadmapItem(
            priority=priority,
            category="Testing",
            action="Add coverage reporting using coverage.py and enforce minimum coverage thresholds.",
            expected_impact="Ensures critical code paths are tested."
        ))
        priority += 1

    # ---- DOCUMENTATION ----
    if not doc.has_readme:
        items.append(RoadmapItem(
            priority=priority,
            category="Documentation",
            action="Create a comprehensive README with overview, setup, and usage examples.",
            expected_impact="Improves usability and recruiter perception."
        ))
        priority += 1
    else:
        if not doc.has_installation:
            items.append(RoadmapItem(
                priority=priority,
                category="Documentation",
                action="Add clear installation instructions to the README.",
                expected_impact="Makes the project easier to run."
            ))
            priority += 1

        if not doc.has_usage:
            items.append(RoadmapItem(
                priority=priority,
                category="Documentation",
                action="Add usage examples and command references.",
                expected_impact="Helps users understand how to use the project."
            ))
            priority += 1

    # ---- CODE QUALITY ----
    if code.pylint_score is not None and code.pylint_score < 7:
        items.append(RoadmapItem(
            priority=priority,
            category="Code Quality",
            action="Resolve pylint warnings and improve coding standards.",
            expected_impact="Improves readability and professional quality."
        ))
        priority += 1

    if code.average_complexity > 5:
        items.append(RoadmapItem(
            priority=priority,
            category="Code Quality",
            action="Refactor high-complexity functions into smaller units.",
            expected_impact="Improves maintainability and scalability."
        ))
        priority += 1

    # ---- CI / DEVOPS ----
    if not structure.has_ci:
        items.append(RoadmapItem(
            priority=priority,
            category="DevOps",
            action="Add a CI pipeline using GitHub Actions to run tests and linters.",
            expected_impact="Prevents broken code from being merged."
        ))
        priority += 1

    # ---- GIT PRACTICES ----
    if git.commit_message_quality == "poor":
        items.append(RoadmapItem(
            priority=priority,
            category="Git Practices",
            action="Adopt meaningful commit messages describing intent.",
            expected_impact="Improves collaboration and traceability."
        ))
        priority += 1

    if not git.has_pull_requests:
        items.append(RoadmapItem(
            priority=priority,
            category="Git Practices",
            action="Use feature branches and pull requests instead of direct commits to main.",
            expected_impact="Encourages review and scalable collaboration."
        ))
        priority += 1

    # ---- GUARANTEED FALLBACK (CRITICAL FIX) ----
    if not items:
        items.append(RoadmapItem(
            priority=1,
            category="General Improvement",
            action="Improve testing, documentation, and code structure following industry best practices.",
            expected_impact="Raises overall project maturity and maintainability."
        ))

    # Ensure correct ordering
    items = sorted(items, key=lambda x: x.priority)

    return ImprovementRoadmap(items=items)
