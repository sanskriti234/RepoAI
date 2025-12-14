import os
from dotenv import load_dotenv

load_dotenv(override=True)

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")



if not GITHUB_TOKEN:
    print("⚠️ WARNING: GITHUB_TOKEN not loaded")
else:
    print("✅ GITHUB_TOKEN loaded")
