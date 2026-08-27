import re
import requests
from bs4 import BeautifulSoup
from tools.web_search import search_web

def is_valid_url(text):
    """Check if the given text is a valid HTTP/HTTPS URL."""
    if not text:
        return False
    text = text.strip()
    return bool(re.match(r'^https?://[^\s]+$', text, re.IGNORECASE))

def scrape_job_url(url):
    """
    Scrape job description content from a posting URL.
    Handles headers, HTML cleanup, and fallback to web search.
    """
    url = url.strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200 and response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts, styles, navigation, headers, footers
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'noscript', 'iframe', 'svg']):
                element.decompose()
            
            text = soup.get_text(separator=' ')
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            
            if len(cleaned_text) > 150:
                return cleaned_text

    except Exception as e:
        print(f"Direct HTTP fetch failed for {url}: {e}. Falling back to web search context...")

    # Fallback: Use Tavily search to fetch site context if direct GET is blocked
    try:
        search_query = f"job description posting {url}"
        tavily_results = search_web(search_query)
        if tavily_results:
            return f"URL: {url}\n\nJob Posting Content:\n{tavily_results}"
    except Exception as e:
        print(f"Fallback web search failed: {e}")

    return f"Job Posting URL: {url}"
