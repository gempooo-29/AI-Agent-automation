import webbrowser
import urllib.parse
import requests
from langchain_core.tools import tool


@tool
def youtube_search(query: str) -> str:
    """
    Search for a video or song on YouTube and open it in the browser.
    Use this when the user asks to play, search, or find a video or song on YouTube.

    Args:
        query: The video or song to search for (e.g. 'Bohemian Rhapsody Queen')

    Returns:
        Confirmation that the video was opened in the browser.
    """
    try:
        # Search YouTube and get first result
        search_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={search_query}"

        # Open in browser
        webbrowser.open(url)

        return f"Opening YouTube search for '{query}' in your browser. ✅"

    except Exception as e:
        return f"Could not open YouTube for '{query}': {str(e)}"