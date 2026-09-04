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

class FriendlyAPIException(Exception):
    """Custom exception containing friendly human-readable messages and suggestions."""
    def __init__(self, message, code=500, hint="Please try again or contact support if the issue persists."):
        super().__init__(message)
        self.message = message
        self.code = code
        self.hint = hint

def map_error_to_friendly_exception(e):
    """Translate raw API and system errors into friendly, professional user messages."""
    err_str = str(e).lower()

    # 401: Invalid API Key / Authentication Failure
    if "401" in err_str or "invalid_api_key" in err_str or "unauthorized" in err_str or "authentication" in err_str:
        return FriendlyAPIException(
            "API Authentication Failed: Invalid or missing API key.",
            code=401,
            hint="Please check that your GROQ_API_KEY environment variable is configured correctly."
        )

    # 403: Forbidden / Missing Scope / Permission Denied
    if "403" in err_str or "forbidden" in err_str or "permission_denied" in err_str or "scope" in err_str:
        return FriendlyAPIException(
            "Access Denied: Insufficient API permissions or model scope.",
            code=403,
            hint="Please verify API key permissions and model access scope."
        )

    # 422: Unprocessable Entity / Invalid Input Data
    if "422" in err_str or "unprocessable" in err_str or "invalid_request" in err_str or "json_validate" in err_str:
        return FriendlyAPIException(
            "Input Processing Error: The document text or prompt format could not be parsed.",
            code=422,
            hint="Please check your resume and job description text for special characters or formatting issues."
        )

    # 429: Rate Limit Exceeded / Credit Exhaustion / Quota Reached
    if "429" in err_str or "rate_limit" in err_str or "credit" in err_str or "quota" in err_str or "tpm" in err_str or "insufficient_quota" in err_str:
        return FriendlyAPIException(
            "Service Busy / Rate Limit Reached: Too many requests or token limit reached.",
            code=429,
            hint="Please wait 10 to 15 seconds before submitting your request again."
        )

    # Network Timeout / Connection Interrupted
    if "timeout" in err_str or "connection" in err_str or "network" in err_str or "connecterror" in err_str or "timeouterror" in err_str:
        return FriendlyAPIException(
            "Network Timeout: Connection to AI processing services timed out.",
            code=504,
            hint="Please check your internet connection and try submitting again."
        )

    # 500 / 502 / 503 / API Unavailable / Webhook Failure
    if "500" in err_str or "502" in err_str or "503" in err_str or "unavailable" in err_str or "overloaded" in err_str or "webhook" in err_str:
        return FriendlyAPIException(
            "AI Service Temporarily Unavailable: The backend service is experiencing traffic or maintenance.",
            code=503,
            hint="Please wait a moment and click Try Again."
        )

    # Generic Friendly Fallback (Never show raw code stack)
    return FriendlyAPIException(
        "Processing Notice: Unable to complete application analysis.",
        code=500,
        hint="Please verify your input files and try again."
    )

def call_groq_completion(messages, model=None, response_format=None, max_retries=5, temperature=0.7, max_tokens=1500):
    """Call Groq API with automatic retry backoff, fallback models, and friendly exception mapping."""
    try:
        client = get_groq_client()
    except Exception as e:
        raise map_error_to_friendly_exception(e)

    target_model = model or config.GROQ_MODEL
    models_to_try = [target_model] + [m for m in FALLBACK_MODELS if m != target_model]

    last_error = None
    for model_idx, current_model in enumerate(models_to_try):
        for attempt in range(max_retries):
            try:
                kwargs = {
                    "model": current_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_completion_tokens": max_tokens
                }
                if response_format:
                    kwargs["response_format"] = response_format
                    
                completion = client.chat.completions.create(**kwargs)
                return completion.choices[0].message.content
            except Exception as e:
                last_error = e
                err_str = str(e)
                if "429" in err_str or "rate_limit" in err_str.lower() or "tpm" in err_str.lower():
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
                elif "401" in err_str or "403" in err_str:
                    # Authentication or permission error; don't retry in loop
                    raise map_error_to_friendly_exception(e)
                else:
                    if attempt < max_retries - 1:
                        time.sleep(2.0)
                        continue

    raise map_error_to_friendly_exception(last_error or Exception("API execution failed"))


