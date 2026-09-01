import requests
from bs4 import BeautifulSoup
import config

def search_web(query, max_results=3):
    """Perform a web search using Tavily if API key exists, otherwise fallback to free search."""
    tavily_key = getattr(config, 'TAVILY_API_KEY', '')
    if tavily_key and tavily_key != 'your_tavily_api_key_here':
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=tavily_key)
            response = client.search(query=query, max_results=max_results)
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', '')
                })
            if results:
                return results
        except Exception as e:
            print(f"Tavily search notice: {e}. Falling back to free search...")

    # Free DuckDuckGo HTML Fallback Search
    try:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet', limit=max_results):
                snippet = a.get_text(strip=True)
                results.append({
                    'title': query,
                    'url': '',
                    'content': snippet
                })
            if results:
                return results
    except Exception as e:
        print(f"Free web search notice: {e}")

    return [{'title': query, 'url': '', 'content': f"Context search query: {query}"}]