import arxiv
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def search_arxiv(query: str, max_results: int = 3) -> list:
    """
    Search ArXiv for papers.
    Returns a list of dicts with keys: title, authors, summary, url, published_date.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for paper in client.results(search):
            authors = [author.name for author in paper.authors]
            results.append({
                'title': paper.title,
                'authors': authors,
                'summary': paper.summary,
                'url': paper.entry_id,
                'published_date': paper.published.isoformat() if paper.published else None
            })
        return results
    except Exception as e:
        print(f"Error searching arxiv: {e}")
        return []
