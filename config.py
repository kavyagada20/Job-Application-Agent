import os
from dotenv import load_dotenv

load_dotenv()

# Change these to Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Please set a valid GROQ_API_KEY in .env")

if not TAVILY_API_KEY:
    raise ValueError("Please set a valid TAVILY_API_KEY in .env")

# Model settings
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")