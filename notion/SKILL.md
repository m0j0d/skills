---
name: notion
description: Notion workspace integration for searching, creating, and managing pages, databases, and collaborative content
tags: [productivity, knowledge-management, collaboration, notion]
created_from: mcp-server
original_server: makenotion/notion-mcp-server
---

# Notion

Comprehensive Notion workspace integration that enables searching, creating, updating, and managing pages, databases, comments, and users directly from Claude Code.

**Based on:** `makenotion/notion-mcp-server` MCP server

## When to Use This Skill

Use this skill when you need to:

- **Search and retrieve content** - Find pages, databases, and content across your Notion workspace
- **Create and manage pages** - Build new pages with rich content, update existing pages, or move pages between locations
- **Database operations** - Create databases, update schemas, and manage database properties
- **Collaboration** - Add comments, list users, and manage team access
- **Content organization** - Duplicate pages, archive content, and restructure workspace hierarchy

## Core Capabilities

### 1. Content Search and Retrieval
Search across your entire Notion workspace and retrieve pages or databases by ID or URL.

### 2. Page Management
Create new pages with rich content blocks, update page properties, move pages, archive/unarchive, and duplicate pages.

### 3. Database Operations
Create databases with custom schemas, update database properties, and manage database structure.

### 4. Collaboration Features
Add comments to pages, retrieve comments, list workspace users, and get user details.

## Available Tools

### `notion_search()`

Search across your Notion workspace for pages and databases.

**Required Parameters:**
- `query` (str) - Search text to find in pages and databases

**Optional Parameters:**
- `filter` (dict) - Filter results by type (page or database)
- `sort` (dict) - Sort options with direction and timestamp

**Returns:** Search results with matching pages and databases

**Example:**
```python
# Basic search
results = notion_search(query="project planning")

# Search only for pages
results = notion_search(
    query="meeting notes",
    filter={"property": "object", "value": "page"}
)

# Search and sort by last edited
results = notion_search(
    query="documentation",
    sort={"direction": "descending", "timestamp": "last_edited_time"}
)
```

### `notion_fetch()`

Retrieve a specific page or database by ID or URL.

**Required Parameters:**
- `page_id` (str) - Page/database ID or full Notion URL

**Returns:** Complete page or database object with properties and content

**Example:**
```python
# Fetch by ID
page = notion_fetch(page_id="12345678-1234-1234-1234-123456789012")

# Fetch by URL
page = notion_fetch(page_id="https://www.notion.so/Page-Title-12345678")
```

### `notion_create_pages()`

Create a new page with content in your Notion workspace.

**Required Parameters:**
- `parent` (dict) - Parent location (page_id or database_id)
- `properties` (dict) - Page properties including title

**Optional Parameters:**
- `children` (list) - Content blocks to add to the page
- `icon` (dict) - Emoji or external icon for the page
- `cover` (dict) - Cover image for the page

**Returns:** Created page object

**Example:**
```python
# Create a simple page
page = notion_create_pages(
    parent={"page_id": "parent-page-id"},
    properties={
        "title": [{"text": {"content": "New Page Title"}}]
    }
)

# Create page with content blocks
page = notion_create_pages(
    parent={"page_id": "parent-page-id"},
    properties={
        "title": [{"text": {"content": "Meeting Notes"}}]
    },
    children=[
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Meeting agenda..."}}]
            }
        }
    ],
    icon={"type": "emoji", "emoji": "📝"}
)
```

### `notion_update_page()`

Update properties or metadata of an existing page.

**Required Parameters:**
- `page_id` (str) - ID of the page to update

**Optional Parameters:**
- `properties` (dict) - Properties to update
- `archived` (bool) - Set archive status
- `icon` (dict) - Update page icon
- `cover` (dict) - Update cover image

**Returns:** Updated page object

**Example:**
```python
# Update page title
page = notion_update_page(
    page_id="page-id",
    properties={
        "title": [{"text": {"content": "Updated Title"}}]
    }
)

# Archive a page
page = notion_update_page(
    page_id="page-id",
    archived=True
)
```

### `notion_move_pages()`

Move a page to a new parent location.

**Required Parameters:**
- `page_id` (str) - ID of the page to move
- `parent` (dict) - New parent location (page_id or database_id)

**Returns:** Updated page object

**Example:**
```python
# Move page to new parent
page = notion_move_pages(
    page_id="page-id",
    parent={"page_id": "new-parent-id"}
)
```

### `notion_create_database()`

Create a new database with a custom schema.

**Required Parameters:**
- `parent` (dict) - Parent page where database will be created
- `properties` (dict) - Database schema with property definitions

**Optional Parameters:**
- `title` (list) - Database title as rich text array

**Returns:** Created database object

**Example:**
```python
# Create a task database
database = notion_create_database(
    parent={"page_id": "parent-page-id"},
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Not Started", "color": "red"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Complete", "color": "green"}
                ]
            }
        },
        "Due Date": {"date": {}}
    },
    title=[{"type": "text", "text": {"content": "Tasks"}}]
)
```

### `notion_update_database()`

Update database schema or metadata.

**Required Parameters:**
- `database_id` (str) - ID of the database to update

**Optional Parameters:**
- `title` (list) - New database title
- `description` (list) - New database description
- `properties` (dict) - Property schema updates

**Returns:** Updated database object

**Example:**
```python
# Update database title
database = notion_update_database(
    database_id="database-id",
    title=[{"type": "text", "text": {"content": "Updated Tasks"}}]
)
```

### `notion_create_comment()`

Add a comment to a page.

**Required Parameters:**
- `page_id` (str) - ID of the page
- `rich_text` (list) - Comment text as rich text array

**Returns:** Created comment object

**Example:**
```python
# Add a comment
comment = notion_create_comment(
    page_id="page-id",
    rich_text=[
        {"type": "text", "text": {"content": "Great work on this page!"}}
    ]
)
```

### `notion_get_comments()`

Retrieve all comments from a page.

**Required Parameters:**
- `page_id` (str) - ID of the page

**Optional Parameters:**
- `start_cursor` (str) - Pagination cursor for next page of results

**Returns:** List of comments with pagination info

**Example:**
```python
# Get all comments on a page
comments = notion_get_comments(page_id="page-id")

# Paginate through comments
next_page = notion_get_comments(
    page_id="page-id",
    start_cursor=comments["next_cursor"]
)
```

### `notion_get_teams()`

Retrieve list of teams (teamspaces) in your workspace.

**Returns:** List of teams

**Example:**
```python
teams = notion_get_teams()
```

### `notion_get_users()`

List all users in your Notion workspace.

**Optional Parameters:**
- `start_cursor` (str) - Pagination cursor

**Returns:** List of users with pagination info

**Example:**
```python
# Get all users
users = notion_get_users()

# Paginate through users
next_page = notion_get_users(start_cursor=users["next_cursor"])
```

### `notion_get_user()`

Get details about a specific user.

**Required Parameters:**
- `user_id` (str) - ID of the user

**Returns:** User object with details

**Example:**
```python
user = notion_get_user(user_id="user-id")
```

### `notion_get_self()`

Get information about the bot integration.

**Returns:** Bot user object

**Example:**
```python
bot_info = notion_get_self()
```

### `notion_duplicate_page()`

Duplicate an existing page.

**Required Parameters:**
- `page_id` (str) - ID of the page to duplicate

**Returns:** Newly created duplicated page object

**Example:**
```python
duplicate = notion_duplicate_page(page_id="page-id")
```

## Setup and Authentication

### Prerequisites

1. **Notion Account** - You need a Notion workspace
2. **Create Integration** - Create a Notion integration at https://www.notion.so/my-integrations
3. **Grant Permissions** - Share pages/databases with your integration

### Configuration

1. **Create a Notion Integration:**
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Give it a name and select capabilities
   - Copy the "Internal Integration Token"

2. **Set environment variable:**
```bash
export NOTION_TOKEN="your_integration_token_here"
```

3. **Share content with integration:**
   - Open the page or database you want to access
   - Click "..." menu → "Add connections"
   - Select your integration

### Required Scopes / Permissions

When creating your integration, configure these capabilities:

- **Read content** - View pages and databases
- **Update content** - Modify existing content
- **Insert content** - Create new pages and databases
- **Read comments** - View page comments
- **Insert comments** - Add new comments
- **Read user information** - Access user details

## Common Workflows

### Search and Update Pages

```python
# Find a page and update it
results = notion_search(query="Weekly Report")

if results["results"]:
    page_id = results["results"][0]["id"]
    notion_update_page(
        page_id=page_id,
        properties={
            "Status": {"select": {"name": "Complete"}}
        }
    )
```

### Create Project Page with Tasks Database

```python
# Create a project page
project = notion_create_pages(
    parent={"page_id": "workspace-root-id"},
    properties={
        "title": [{"text": {"content": "Q1 Planning"}}]
    },
    icon={"type": "emoji", "emoji": "📊"}
)

# Add a tasks database to the project
database = notion_create_database(
    parent={"page_id": project["id"]},
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Todo", "color": "red"},
                    {"name": "Done", "color": "green"}
                ]
            }
        }
    },
    title=[{"type": "text", "text": {"content": "Tasks"}}]
)
```

### Bulk Comment on Pages

```python
# Search for pages and add comments
results = notion_search(query="review needed")

for page in results["results"]:
    notion_create_comment(
        page_id=page["id"],
        rich_text=[
            {"type": "text", "text": {"content": "Reviewed and approved"}}
        ]
    )
```

## Implementation Notes

- **URL handling** - The skill automatically extracts page IDs from Notion URLs
- **Pagination** - Many endpoints return paginated results; use `start_cursor` for next page
- **Rich text format** - Notion uses rich text arrays for formatted content
- **Rate limiting** - Notion API has a rate limit of 3 requests per second (180/minute)
- **Dual fetch** - `notion_fetch()` tries both page and database endpoints automatically

## Error Handling

Common error scenarios and solutions:

- **Authentication failed:** Check that `NOTION_TOKEN` is set correctly
- **Page not found:** Verify the integration has access to the page (must be shared)
- **Invalid parent:** Ensure parent page/database exists and is accessible
- **Rate limit exceeded:** Implement delays between requests (333ms minimum)
- **Invalid properties:** Check that property types match the database schema

## Security Best Practices

1. **Token security** - Store `NOTION_TOKEN` in environment variables, never in code
2. **Minimal access** - Only share necessary pages with your integration
3. **Read-only when possible** - Create separate integrations for read vs write operations
4. **Audit access** - Regularly review which pages are shared with integrations
5. **Rotate tokens** - Periodically regenerate integration tokens

## Cost Considerations

**IMPORTANT:** Notion API has rate limits that affect skill usage.

### Rate Limits

Notion enforces the following rate limits:

- **3 requests per second** - Hard limit per integration
- **180 requests per minute** - Effective rate limit
- **No daily quota** - Unlimited requests within rate limits

**Best practices:**
- Add 333ms delay between requests to stay within limits
- Batch operations when possible to reduce API calls
- Cache frequently accessed content
- Use search filters to reduce result sets

### Notion Plans

- **Free Plan:** Full API access with rate limits
- **Paid Plans:** Same API access (no quota differences)
- **Enterprise:** May have higher rate limits (contact Notion)

**Note:** The Notion API is free to use regardless of plan tier, subject to rate limits.
