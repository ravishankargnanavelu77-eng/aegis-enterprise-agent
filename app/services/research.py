from tavily import TavilyClient

from app.core.config import get_settings


def search_web(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """Search the web and return normalized research results."""

    settings = get_settings()

    client = TavilyClient(
        api_key=settings.tavily_api_key,
    )

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )

    results = []

    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
        )

    return results
