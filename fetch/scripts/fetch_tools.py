#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Web content fetching with HTML-to-markdown conversion.
Based on @modelcontextprotocol/server-fetch MCP server.
"""

import json
import sys
from typing import Dict, Any
try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    print("Error: Required packages not installed. Run: pip install requests beautifulsoup4 html2text", file=sys.stderr)
    sys.exit(1)


def fetch(url: str, max_length: int = 5000, start_index: int = 0, raw: bool = False) -> Dict[str, Any]:
    """
    Fetch web content and optionally convert to markdown.

    Args:
        url: Web address to fetch
        max_length: Maximum characters to return (default: 5000)
        start_index: Starting position for chunked reading (default: 0)
        raw: Return raw HTML instead of markdown (default: False)

    Returns:
        Result with content
    """
    try:
        # Fetch URL
        headers = {
            'User-Agent': 'Claude-Code-Fetch-Skill/1.0'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        content = response.text

        # Convert to markdown unless raw requested
        if not raw:
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            content = h.handle(content)

        # Apply chunking
        if start_index > 0:
            content = content[start_index:]

        if max_length > 0:
            content = content[:max_length]
            truncated = len(response.text) > (start_index + max_length)
        else:
            truncated = False

        return {
            'status': 'success',
            'tool': 'fetch',
            'url': url,
            'content': content,
            'length': len(content),
            'truncated': truncated,
            'next_index': start_index + len(content) if truncated else None
        }

    except requests.RequestException as e:
        return {
            'status': 'error',
            'tool': 'fetch',
            'message': f'Failed to fetch URL: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'fetch',
            'message': str(e)
        }


# CLI interface
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python fetch_tools.py fetch <url> [max_length] [start_index] [raw]")
        sys.exit(1)

    tool_name = sys.argv[1]
    if tool_name != 'fetch':
        print(f"Unknown tool: {tool_name}")
        sys.exit(1)

    url = sys.argv[2]
    max_length = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    start_index = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    raw = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False

    result = fetch(url, max_length, start_index, raw)
    print(json.dumps(result, indent=2))
