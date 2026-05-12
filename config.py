<<<<<<< HEAD
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
# llama-3.3-70b-versatile is a strong choice for complex reasoning
=======
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
# llama-3.3-70b-versatile is a strong choice for complex reasoning
>>>>>>> 06116eaa0f9be49c8fcaabd5f2720b3ecc5dc093
GROQ_MODEL = "llama-3.3-70b-versatile"