import json
import re

def extract_json(text: str) -> dict:
    """
    Extract first JSON object from LLM output safely.
    """
    # Remove markdown fences if present
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    # Find JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_str = match.group(0)

    return json.loads(json_str)
