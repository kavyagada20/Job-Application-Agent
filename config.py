import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

if not GROQ_API_KEY:
    raise ValueError("Please set a valid GROQ_API_KEY in your environment or .env file")

# High-capacity model with 100,000 TPM limit on Groq Free Tier
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")