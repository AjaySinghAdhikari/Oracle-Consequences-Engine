import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Ensure environment variables are loaded
load_dotenv()

def search_web(query: str, max_results: int = 5) -> list:
    """
    Search the web using Tavily.
    Returns a list of dicts with keys: title, url, content, score.
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("Warning: TAVILY_API_KEY not found in environment.")
            return []
            
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        
        results = []
        for res in response.get('results', []):
            results.append({
                'title': res.get('title', ''),
                'url': res.get('url', ''),
                'content': res.get('content', ''),
                'score': res.get('score', 0.0)
            })
        return results
    except Exception as e:
        print(f"Error searching web with Tavily: {e}")
        return []
