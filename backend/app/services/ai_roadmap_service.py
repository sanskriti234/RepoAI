import os
import json
from groq import Groq
from backend.app.models.analysis_models import (
    ImprovementRoadmap,
    RoadmapItem
)

# =========================================================
# Initialize Groq Client
# =========================================================

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================================================
# Prompt Builder (RULE-DRIVEN & DYNAMIC)
# =========================================================

def build_roadmap_prompt(
    repo_name,
    score,
    structure,
    code,
    doc,
    testing,
    git
) -> str:
    return f"""
You are a senior software engineer acting as a strict technical mentor.

Repository Name: {repo_name}

FACTS (you MUST rely only on these facts):
- Overall Score: {score.total_score}/100 ({score.level})
- Structure:
    - CI present: {structure.has_ci}
    - Max directory depth: {structure.max_depth}
- Code Quality:
    - Pylint score: {code.pylint_score}
    - Average cyclomatic complexity: {code.average_complexity}
- Documentation:
    - README exists: {doc.has_readme}
    - Installation instructions: {doc.has_installation}
    - Usage instructions: {doc.has_usage}
- Testing:
    - Tests present: {testing.has_tests}
    - Number of test files: {testing.test_files_count}
- Git Practices:
    - Total commits: {git.total_commits}
    - Commit message quality: {git.commit_message_quality}
    - Pull requests used: {git.has_pull_requests}

MANDATORY DECISION RULES:
- If tests are missing → Testing MUST be priority 1
- If avg complexity > 10 → Refactoring MUST be included
- If CI is missing → CI/CD improvement MUST be included
- If README exists but lacks install/usage → Documentation improvement required
- If commit message quality is poor → Git practices improvement required
- Maximum 6 roadmap items
- Order strictly by highest impact first
- Be concise and actionable
- DO NOT praise the repository
- DO NOT invent missing data

TASK:
Generate a personalized improvement roadmap for THIS repository.

OUTPUT FORMAT (STRICT):
Return ONLY a valid JSON array.

Example:
[
  {{
    "priority": 1,
    "category": "Testing",
    "action": "Add unit tests using pytest for core business logic",
    "expected_impact": "Reduces regressions and increases confidence in changes"
  }}
]
"""

# =========================================================
# Main Roadmap Generator
# =========================================================

def generate_dynamic_roadmap(
    repo_name,
    score,
    structure,
    code,
    doc,
    testing,
    git
) -> ImprovementRoadmap:

    prompt = build_roadmap_prompt(
        repo_name,
        score,
        structure,
        code,
        doc,
        testing,
        git
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # HIGH reasoning model
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict senior software engineer who follows rules exactly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        raw_text = response.choices[0].message.content.strip()

        # 🔥 CRITICAL FIX: Use json.loads(), not eval()
        raw_items = json.loads(raw_text)

        items = []
        for item in raw_items:
            items.append(
                RoadmapItem(
                    priority=item["priority"],
                    category=item["category"],
                    action=item["action"],
                    expected_impact=item["expected_impact"]
                )
            )

        return ImprovementRoadmap(items=items)

    except Exception as e:
        print("[ROADMAP GENERATION FAILED - FALLBACK USED]", e)
        return fallback_roadmap(score, structure, code, testing, doc, git)

# =========================================================
# Intelligent Fallback (Repo-Aware)
# =========================================================

def fallback_roadmap(score, structure, code, testing, doc, git) -> ImprovementRoadmap:
    items = []
    priority = 1

    if not testing.has_tests:
        items.append(RoadmapItem(
            priority=priority,
            category="Testing",
            action="Introduce automated unit tests for core modules using pytest.",
            expected_impact="Improves reliability and prevents regressions."
        ))
        priority += 1

    if code.average_complexity and code.average_complexity > 10:
        items.append(RoadmapItem(
            priority=priority,
            category="Code Quality",
            action="Refactor high-complexity functions into smaller, testable units.",
            expected_impact="Improves readability, maintainability, and testability."
        ))
        priority += 1

    if not structure.has_ci:
        items.append(RoadmapItem(
            priority=priority,
            category="CI/CD",
            action="Add a CI pipeline (GitHub Actions) for linting and test execution.",
            expected_impact="Ensures consistent quality checks on every commit."
        ))
        priority += 1

    if doc.has_readme and not (doc.has_installation and doc.has_usage):
        items.append(RoadmapItem(
            priority=priority,
            category="Documentation",
            action="Enhance README with clear installation and usage instructions.",
            expected_impact="Reduces onboarding friction for users and contributors."
        ))
        priority += 1

    if git.commit_message_quality == "poor":
        items.append(RoadmapItem(
            priority=priority,
            category="Git Practices",
            action="Adopt conventional commit messages and enforce them via hooks.",
            expected_impact="Improves project history clarity and collaboration."
        ))
        priority += 1

    if not items:
        items.append(RoadmapItem(
            priority=1,
            category="General",
            action="Incrementally improve testing, documentation, and code quality.",
            expected_impact="Gradually increases overall project maturity."
        ))

    return ImprovementRoadmap(items=items)
