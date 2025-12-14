from backend.app.models.analysis_models import ImprovementRoadmap, RoadmapItem
import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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
You are a senior software engineer acting as a technical mentor.

Repository: {repo_name}

FACTS (do not invent anything):
- Overall score: {score.total_score}/100 ({score.level})
- Structure: has CI = {structure.has_ci}, depth = {structure.max_depth}
- Code quality: pylint score = {code.pylint_score}, avg complexity = {code.average_complexity}
- Documentation: README = {doc.has_readme}, install = {doc.has_installation}, usage = {doc.has_usage}
- Testing: has tests = {testing.has_tests}, test files = {testing.test_files_count}
- Git: commits = {git.total_commits}, commit quality = {git.commit_message_quality}, PRs = {git.has_pull_requests}

TASK:
Generate a personalized improvement roadmap for THIS repository.

Rules:
- Use ONLY the facts above
- Do NOT praise unnecessarily
- Prioritize highest-impact improvements first
- Roadmap must be realistic and actionable
- Max 6 steps
- Each step should improve repo quality measurably

FORMAT (STRICT JSON ARRAY ONLY):
[
  {{
    "priority": 1,
    "category": "Testing",
    "action": "Add unit tests using pytest for core modules",
    "expected_impact": "Improves reliability and confidence in changes"
  }}
]
"""


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
        repo_name, score, structure, code, doc, testing, git
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict senior software engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        raw_items = eval(response.choices[0].message.content)

        items = [
            RoadmapItem(
                priority=item["priority"],
                category=item["category"],
                action=item["action"],
                expected_impact=item["expected_impact"]
            )
            for item in raw_items
        ]

        return ImprovementRoadmap(items=items)

    except Exception as e:
        print("[GROQ ROADMAP FALLBACK]", e)
        return fallback_roadmap(score, testing, doc, git)


def fallback_roadmap(score, testing, doc, git) -> ImprovementRoadmap:
    items = []

    if not testing.has_tests:
        items.append(RoadmapItem(
            priority=1,
            category="Testing",
            action="Introduce automated tests for core functionality.",
            expected_impact="Improves reliability and prevents regressions."
        ))

    if git.commit_message_quality == "poor":
        items.append(RoadmapItem(
            priority=2,
            category="Git Practices",
            action="Improve commit message clarity and consistency.",
            expected_impact="Improves maintainability and collaboration."
        ))

    if not items:
        items.append(RoadmapItem(
            priority=1,
            category="General",
            action="Gradually improve testing, structure, and code quality.",
            expected_impact="Raises overall project maturity."
        ))

    return ImprovementRoadmap(items=items)
