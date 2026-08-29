import time
from groq import Groq
import config

_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client

def call_groq_completion(messages, model=None, response_format=None, max_retries=4, temperature=0.7):
    """Call Groq API with automatic retry backoff for rate limits (429)."""
    client = get_groq_client()
    target_model = model or config.GROQ_MODEL
    
    for attempt in range(max_retries):
        try:
            kwargs = {
                "model": target_model,
                "messages": messages,
                "temperature": temperature
            }
            if response_format:
                kwargs["response_format"] = response_format
                
            completion = client.chat.completions.create(**kwargs)
            return completion.choices[0].message.content
        except Exception as e:
            err_str = str(e)
            if ("429" in err_str or "rate_limit" in err_str.lower() or "tpm" in err_str.lower()) and attempt < max_retries - 1:
                wait_time = 3.0 * (attempt + 1)
                print(f"Groq Rate Limit notice (Attempt {attempt+1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise e
