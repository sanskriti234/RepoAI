import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_repo_explanation_prompt(repo_name: str, readme_text: str) -> str:
    return f"""
You are a senior software engineer explaining a GitHub project.

Repository: {repo_name}

README CONTENT:
\"\"\"
{readme_text}
\"\"\"

TASK:
Generate a detailed explanation with the following sections:

1. Project Purpose
2. Problem It Solves
3. Core Components / Modules
4. How the System Works (step-by-step flow)
5. Typical Use Case

Rules:
- Use ONLY README information
- Do NOT invent features
- Keep explanation technical but simple
- Avoid marketing language

FORMAT STRICT JSON:
{{
  "purpose": "...",
  "problem": "...",
  "components": ["...", "..."],
  "workflow": ["Step 1 ...", "Step 2 ..."],
  "use_case": "..."
}}
"""


def fallback_repo_explanation(readme_text: str) -> str:
    lines = readme_text.splitlines()
    short_text = " ".join(lines[:10])

    return (
        "This repository appears to be a software project described in the README. "
        "Based on the available documentation, it provides functionality related to the problem domain mentioned. "
        "However, detailed explanation of its internal working is limited."
    )


import json

from backend.app.utils.json_extractor import extract_json

def generate_repo_explanation(repo_name: str, readme_text: str) -> dict:
    if not readme_text.strip():
        return {
            "purpose": "README is empty or missing.",
            "problem": "README is empty or missing.",
            "components": [],
            "workflow": [],
            "use_case": "Not specified."
        }

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You explain software systems clearly and respond ONLY with JSON."
                },
                {
                    "role": "user",
                    "content": build_repo_explanation_prompt(repo_name, readme_text)
                }
            ],
            temperature=0.1
        )

        raw_text = response.choices[0].message.content

        # 🔍 VERY IMPORTANT DEBUG
        print("DEBUG RAW MODEL OUTPUT:\n", raw_text)

        return extract_json(raw_text)

    except Exception as e:
        print("[REPO EXPLANATION FALLBACK]", e)
        return {
            "purpose": "Explanation unavailable.",
            "problem": "Explanation unavailable.",
            "components": [],
            "workflow": [],
            "use_case": "Explanation unavailable."
        }

    