"""Free web tools exposed to DeepSeek as function calls.

DeepSeek has no built-in browsing, so we provide:
- web_search via DuckDuckGo HTML endpoint (no key required)
- fetch_url via plain requests with light HTML→text cleanup

These are intentionally simple. If rate-limited, swap in Tavily / Brave / SerpAPI.
"""

from __future__ import annotations
import re
import time
from typing import Any
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})


def web_search(query: str, max_results: int = 8) -> list[dict[str, str]]:
    """DuckDuckGo HTML search. Returns [{title, url, snippet}, ...]."""
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    try:
        r = SESSION.get(url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        return [{"error": f"search failed: {e}"}]

    soup = BeautifulSoup(r.text, "html.parser")
    results: list[dict[str, str]] = []
    for node in soup.select("div.result, div.web-result")[:max_results]:
        title_el = node.select_one("a.result__a, h2 a")
        snippet_el = node.select_one(".result__snippet, .snippet")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
        results.append({"title": title, "url": href, "snippet": snippet})

    if not results:
        return [{"warning": "no results parsed (DuckDuckGo may have changed markup)"}]
    return results


def fetch_url(url: str, max_chars: int = 8000) -> dict[str, Any]:
    """Fetch a URL and return cleaned text. Trimmed to max_chars."""
    try:
        r = SESSION.get(url, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        return {"url": url, "error": f"fetch failed: {e}"}

    ctype = r.headers.get("Content-Type", "")
    if "html" not in ctype and "xml" not in ctype:
        # Return raw text (JSON, plain, etc) trimmed
        return {"url": url, "content_type": ctype, "text": r.text[:max_chars]}

    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n", strip=True))
    return {
        "url": url,
        "content_type": ctype,
        "text": text[:max_chars],
        "truncated": len(text) > max_chars,
    }


# ---- Tool schema (OpenAI/DeepSeek function-calling format) ----

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web via DuckDuckGo and return up to 8 results with "
                "title, url, snippet. Use for catalysts, earnings dates, "
                "supply chain news, social sentiment."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "description": "1-10, default 8",
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": (
                "Fetch a URL and return cleaned page text (HTML stripped). "
                "Use after web_search to read full content of a specific article."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Absolute URL"},
                    "max_chars": {
                        "type": "integer",
                        "description": "Max chars to return (default 8000)",
                        "minimum": 500,
                        "maximum": 30000,
                    },
                },
                "required": ["url"],
            },
        },
    },
]

# Dispatch map for tool execution
DISPATCH = {
    "web_search": web_search,
    "fetch_url": fetch_url,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> Any:
    """Run a tool by name. Catches exceptions and returns them as data."""
    fn = DISPATCH.get(name)
    if fn is None:
        return {"error": f"unknown tool: {name}"}
    try:
        return fn(**arguments)
    except TypeError as e:
        return {"error": f"bad arguments for {name}: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"error": f"{name} raised: {e}"}
