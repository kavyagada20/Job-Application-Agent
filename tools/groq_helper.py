import re
import time
from groq import Groq
import config

_client = None

FALLBACK_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b", "groq/compound"]

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client

def call_groq_completion(messages, model=None, response_format=None, max_retries=5, temperature=0.7):
    """Call Groq API with automatic retry backoff and fallback models for rate limits (429)."""
    client = get_groq_client()
    target_model = model or config.GROQ_MODEL
    
    models_to_try = [target_model] + [m for m in FALLBACK_MODELS if m != target_model]

    for model_idx, current_model in enumerate(models_to_try):
        for attempt in range(max_retries):
            try:
                kwargs = {
                    "model": current_model,
                    "messages": messages,
                    "temperature": temperature
                }
                if response_format:
                    kwargs["response_format"] = response_format
                    
                completion = client.chat.completions.create(**kwargs)
                return completion.choices[0].message.content
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate_limit" in err_str.lower() or "tpm" in err_str.lower():
                    # Parse Groq's requested wait time from error message (e.g. "try again in 14.5s")
                    match = re.search(r'try again in (\d+(?:\.\d+)?)s', err_str, re.IGNORECASE)
                    if match:
                        wait_time = float(match.group(1)) + 1.0
                    else:
                        wait_time = 5.0 * (attempt + 1)

                    if attempt < max_retries - 1:
                        print(f"Groq Rate Limit on {current_model} (Attempt {attempt+1}/{max_retries}). Retrying in {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue
                    elif model_idx < len(models_to_try) - 1:
                        print(f"Switching fallback model from {current_model} to {models_to_try[model_idx + 1]} due to rate limits...")
                        time.sleep(2.0)
                        break
                raise e

