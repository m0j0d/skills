#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Wrapper functions for notion MCP server tools.
Auto-generated from MCP server specification.

This module provides Python functions that replicate the functionality
of the notion MCP server, allowing it to be used as a skill without
requiring the original MCP server connection.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
import requests


# Notion API configuration
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"


def _get_headers() -> Dict[str, str]:
    """Get headers for Notion API requests."""
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN environment variable not set")

    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json"
    }


def _make_request(method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
    """Make a request to the Notion API."""
    url = f"{NOTION_API_BASE}/{endpoint}"
    headers = _get_headers()

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {
            "error": True,
            "status_code": e.response.status_code,
            "message": str(e),
            "details": e.response.text
        }
    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }


def _extract_page_id(page_id: str) -> str:
    """Extract page ID from URL or ID string."""
    # If it's a URL, extract the ID
    if "notion.so/" in page_id or "notion.site/" in page_id:
        # Extract ID from URL (last part after /)
        parts = page_id.rstrip('/').split('/')
        page_id = parts[-1]
        # Remove query parameters
        if '?' in page_id:
            page_id = page_id.split('?')[0]
        # Extract just the ID part (32 chars)
        if '-' in page_id:
            page_id = page_id.split('-')[-1]

    # Remove any dashes and format as UUID
    page_id = page_id.replace('-', '')
    if len(page_id) == 32:
        # Format as UUID: 8-4-4-4-12
        page_id = f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"

    return page_id


def notion_search(query: str, filter: Dict = None, sort: Dict = None) -> Dict[str, Any]:
    """
    Search across Notion workspace

    Args:
        query: Search text
        filter: Filter by type (page/database)
        sort: Sort options with direction and timestamp

    Returns:
        Search results from Notion API
    """
    data = {"query": query}
    if filter:
        data["filter"] = filter
    if sort:
        data["sort"] = sort

    return _make_request("POST", "search", data)


def notion_fetch(page_id: str) -> Dict[str, Any]:
    """
    Retrieve page or database content by ID or URL

    Args:
        page_id: Page/database ID or full Notion URL

    Returns:
        Page or database content
    """
    page_id = _extract_page_id(page_id)

    # Try to fetch as page first
    result = _make_request("GET", f"pages/{page_id}")

    # If error, try as database
    if result.get("error"):
        result = _make_request("GET", f"databases/{page_id}")

    return result


def notion_create_pages(parent: Dict, properties: Dict, children: List = None, icon: Dict = None, cover: Dict = None) -> Dict[str, Any]:
    """
    Create new page with content

    Args:
        parent: Parent page_id or database_id
        properties: Page properties including title
        children: Content blocks
        icon: Emoji or external icon
        cover: Cover image

    Returns:
        Created page object
    """
    data = {
        "parent": parent,
        "properties": properties
    }
    if children:
        data["children"] = children
    if icon:
        data["icon"] = icon
    if cover:
        data["cover"] = cover

    return _make_request("POST", "pages", data)


def notion_update_page(page_id: str, properties: Dict = None, archived: bool = None, icon: Dict = None, cover: Dict = None) -> Dict[str, Any]:
    """
    Update page properties or metadata

    Args:
        page_id: Page ID
        properties: Properties to update
        archived: Archive status
        icon: New icon
        cover: New cover

    Returns:
        Updated page object
    """
    page_id = _extract_page_id(page_id)

    data = {}
    if properties is not None:
        data["properties"] = properties
    if archived is not None:
        data["archived"] = archived
    if icon is not None:
        data["icon"] = icon
    if cover is not None:
        data["cover"] = cover

    return _make_request("PATCH", f"pages/{page_id}", data)


def notion_move_pages(page_id: str, parent: Dict) -> Dict[str, Any]:
    """
    Move page to new parent location

    Args:
        page_id: Page ID
        parent: New parent page_id or database_id

    Returns:
        Updated page object
    """
    page_id = _extract_page_id(page_id)

    data = {"parent": parent}
    return _make_request("PATCH", f"pages/{page_id}", data)


def notion_create_database(parent: Dict, properties: Dict, title: List = None) -> Dict[str, Any]:
    """
    Create new database with schema

    Args:
        parent: Parent page
        properties: Database schema definitions
        title: Database title as rich text

    Returns:
        Created database object
    """
    data = {
        "parent": parent,
        "properties": properties
    }
    if title:
        data["title"] = title

    return _make_request("POST", "databases", data)


def notion_update_database(database_id: str, title: List = None, description: List = None, properties: Dict = None) -> Dict[str, Any]:
    """
    Update database schema or metadata

    Args:
        database_id: Database ID
        title: New title
        description: New description
        properties: Property updates

    Returns:
        Updated database object
    """
    database_id = _extract_page_id(database_id)

    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if properties is not None:
        data["properties"] = properties

    return _make_request("PATCH", f"databases/{database_id}", data)


def notion_create_comment(page_id: str, rich_text: List) -> Dict[str, Any]:
    """
    Add comment to page

    Args:
        page_id: Page ID
        rich_text: Comment text as rich text array

    Returns:
        Created comment object
    """
    page_id = _extract_page_id(page_id)

    data = {
        "parent": {"page_id": page_id},
        "rich_text": rich_text
    }

    return _make_request("POST", "comments", data)


def notion_get_comments(page_id: str, start_cursor: str = None) -> Dict[str, Any]:
    """
    Retrieve page comments

    Args:
        page_id: Page ID
        start_cursor: Pagination cursor

    Returns:
        List of comments
    """
    page_id = _extract_page_id(page_id)

    params = {"block_id": page_id}
    if start_cursor:
        params["start_cursor"] = start_cursor

    return _make_request("GET", "comments", params)


def notion_get_teams() -> Dict[str, Any]:
    """
    Retrieve list of teams (teamspaces)

    Returns:
        List of teams
    """
    # Note: This endpoint may not be available in all Notion API versions
    # Fallback to empty list if not supported
    result = _make_request("GET", "teams")
    if result.get("error") and result.get("status_code") == 404:
        return {"results": [], "message": "Teams endpoint not available"}
    return result


def notion_get_users(start_cursor: str = None) -> Dict[str, Any]:
    """
    List all workspace users

    Args:
        start_cursor: Pagination cursor

    Returns:
        List of users
    """
    params = {}
    if start_cursor:
        params["start_cursor"] = start_cursor

    return _make_request("GET", "users", params)


def notion_get_user(user_id: str) -> Dict[str, Any]:
    """
    Get specific user details

    Args:
        user_id: User ID

    Returns:
        User object
    """
    return _make_request("GET", f"users/{user_id}")


def notion_get_self() -> Dict[str, Any]:
    """
    Get bot integration information

    Returns:
        Bot user object
    """
    return _make_request("GET", "users/me")


def notion_duplicate_page(page_id: str) -> Dict[str, Any]:
    """
    Duplicate an existing page

    Args:
        page_id: Page ID to duplicate

    Returns:
        Duplicated page object
    """
    page_id = _extract_page_id(page_id)

    # Notion API doesn't have a direct duplicate endpoint
    # We need to fetch the page and create a new one
    # This is a simplified implementation
    page = _make_request("GET", f"pages/{page_id}")

    if page.get("error"):
        return page

    # Extract parent and properties
    parent = page.get("parent")
    properties = page.get("properties", {})

    # Create new page with same properties
    return notion_create_pages(parent=parent, properties=properties)


if __name__ == "__main__":
    """Command-line interface for tool execution."""

    if len(sys.argv) < 2:
        print("Usage: python notion_tools.py <tool_name> [--param value ...]")
        print("\nAvailable tools:")
        print("  notion_search: Search across Notion workspace")
        print("  notion_fetch: Retrieve page or database content by ID or URL")
        print("  notion_create_pages: Create new page with content")
        print("  notion_update_page: Update page properties or metadata")
        print("  notion_move_pages: Move page to new parent location")
        print("  notion_create_database: Create new database with schema")
        print("  notion_update_database: Update database schema or metadata")
        print("  notion_create_comment: Add comment to page")
        print("  notion_get_comments: Retrieve page comments")
        print("  notion_get_teams: Retrieve list of teams (teamspaces)")
        print("  notion_get_users: List all workspace users")
        print("  notion_get_user: Get specific user details")
        print("  notion_get_self: Get bot integration information")
        print("  notion_duplicate_page: Duplicate an existing page")
        sys.exit(1)

    tool_name = sys.argv[1]

    # Parse parameters
    params = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            param_name = sys.argv[i][2:]
            if i + 1 < len(sys.argv):
                param_value = sys.argv[i + 1]
                # Try to parse JSON for complex types
                try:
                    params[param_name] = json.loads(param_value)
                except json.JSONDecodeError:
                    params[param_name] = param_value
                i += 2
            else:
                print(f"Error: Missing value for parameter {param_name}")
                sys.exit(1)
        else:
            i += 1

    # Execute tool
    try:
        tool_func = globals().get(tool_name)
        if tool_func:
            result = tool_func(**params)
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: Unknown tool '{tool_name}'")
            sys.exit(1)
    except Exception as e:
        print(f"Error executing tool: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
