from backend.app.models.analysis_models import ScoreBreakdown


def build_summary_prompt(
    repo_name: str,
    score: ScoreBreakdown,
    structure,
    code,
    doc,
    testing,
    git
) -> str:
    return f"""
You are a senior software engineer reviewing a GitHub repository.

Repository: {repo_name}

FACTS (do not invent anything):
- Total Score: {score.total_score}/100 ({score.level})
- Structure score: {score.structure}/15
- Code quality score: {score.code_quality}/25
- Documentation score: {score.documentation}/15
- Testing score: {score.testing}/15
- Git practices score: {score.git_practices}/15

Details:
- README present: {doc.has_readme}
- Installation instructions: {doc.has_installation}
- Usage instructions: {doc.has_usage}
- Tests present: {testing.has_tests}
- Test files: {testing.test_files_count}
- Average code complexity: {code.average_complexity}
- Pylint score: {code.pylint_score}
- Commit message quality: {git.commit_message_quality}
- Actively maintained: {git.is_actively_maintained}

TASK:
Write a concise, honest 3–5 line evaluation as a senior engineer.
- Mention strengths first
- Clearly state weaknesses
- Do NOT praise unnecessarily
- Do NOT suggest improvements yet
- Do NOT mention scores explicitly
- Sound professional and realistic
"""

from groq import Groq
from backend.app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)



def generate_summary(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # free + fast
        messages=[
            {"role": "system", "content": "You are a strict senior software engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()


def generate_repo_summary(
    repo_name: str,
    score,
    structure,
    code,
    doc,
    testing,
    git
) -> str:
    prompt = build_summary_prompt(
        repo_name, score, structure, code, doc, testing, git
    )

    try:
        return generate_summary(prompt)
    except Exception as e:
        # Log error in real system
        print(f"[AI SUMMARY FALLBACK] {e}")
        return fallback_summary(score, doc, testing, git)


def fallback_summary(score, doc, testing, git) -> str:
    lines = []

    if score.level == "Advanced":
        lines.append("This repository demonstrates strong engineering practices and a mature structure.")
    elif score.level == "Intermediate":
        lines.append("This repository shows a reasonable level of organization and code quality.")
    else:
        lines.append("This repository reflects an early-stage or learning-focused project.")

    if not testing.has_tests:
        lines.append("The absence of automated tests reduces confidence in long-term maintainability.")

    if not doc.has_readme:
        lines.append("Documentation is minimal, which makes onboarding and usage harder.")

    if not git.is_actively_maintained:
        lines.append("The project does not appear to be actively maintained.")

    return " ".join(lines)
