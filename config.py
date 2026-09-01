import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

if not GROQ_API_KEY:
    raise ValueError("Please set a valid GROQ_API_KEY in your environment or .env file")

# Fast, high-capacity active model on Groq (sub-2s responses)
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")