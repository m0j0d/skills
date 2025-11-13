---
name: fetch
description: Web content fetching with HTML-to-markdown conversion. Retrieve web pages, handle chunked reading for long content, and extract clean text for LLM consumption.
tags: [productivity, web, http, content-retrieval]
created_from: mcp-server
last_validated: 2025-10-25
version: 1.0.0
---

# Fetch - Web Content Retrieval

Fetch web content and convert to markdown for efficient LLM processing. Based on @modelcontextprotocol/server-fetch.

## Installation

This skill requires Python packages for web scraping:

```bash
pip install requests beautifulsoup4 html2text
# Or using requirements file:
pip install -r productivity-skills/fetch/requirements.txt
```

## When to Use

- Research and documentation gathering
- Web scraping for information
- Content extraction from URLs
- Reading documentation sites

## Tools

### fetch

Retrieve URL content and convert to markdown.

**Parameters:**
- `url` (string, required): Web address to fetch
- `max_length` (number, optional): Character limit (default: 5000)
- `start_index` (number, optional): Start position for chunked reading
- `raw` (boolean, optional): Return raw HTML instead of markdown

**Returns:** Web content as markdown (or raw HTML if requested)

**Example:**
```python
fetch(url="https://example.com", max_length=5000)
fetch(url="https://example.com", start_index=5000, max_length=5000)  # Next chunk
fetch(url="https://example.com", raw=True)  # Raw HTML
```

## Features

- **Chunked Reading**: Handle long pages with start_index pagination
- **Markdown Conversion**: Clean, LLM-friendly text format
- **Raw Mode**: Access original HTML when needed
- **Length Control**: Limit response size

## Best Practices

- Use max_length to control response size
- For long pages, fetch in chunks using start_index
- Convert to markdown for better LLM understanding
- Check robots.txt compliance (respect website policies)
