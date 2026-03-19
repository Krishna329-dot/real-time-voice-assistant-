import os
import requests
from livekit.agents import function_tool

GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


@function_tool
async def google_search(query: str) -> str:
    print(f"[TOOL] google_search called")
    print(f"[TOOL] Query: {query}")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"[TOOL] Request failed: {e}")
        return "Search failed due to a network error."

    print(f"[TOOL] HTTP Status: {response.status_code}")

    if response.status_code != 200:
        print(f"[TOOL] Response text: {response.text}")
        return "Search failed due to an API error."

    data = response.json()
    items = data.get("items", [])

    if not items:
        print("[TOOL] No results found")
        return "No relevant results found."

    results = []
    for idx, item in enumerate(items, start=1):
        title = item.get("title")
        snippet = item.get("snippet")
        print(f"[TOOL] Result {idx}: {title}")
        results.append(f"{title}: {snippet}")

    print("[TOOL] google_search completed successfully")
    return " | ".join(results)
