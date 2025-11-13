---
name: linear
description: Linear project management integration for creating, updating, and managing issues, projects, and teams
tags: [productivity, project-management, issue-tracking, linear]
created_from: mcp-server
original_server: jerhadf/linear-mcp-server
---

# Linear

Comprehensive Linear project management integration that enables creating, updating, and managing issues, projects, teams, and comments directly from Claude Code.

**Based on:** `jerhadf/linear-mcp-server` MCP server

## When to Use This Skill

Use this skill when you need to:

- **Issue management** - Create, update, search, and track issues across your Linear workspace
- **Project tracking** - Create projects, manage milestones, and organize work
- **Team collaboration** - View team information, workflow states, and member assignments
- **Automated workflows** - Bulk update issues, automated comments, and status tracking
- **Integration** - Connect Linear with other development tools and processes

## Core Capabilities

### 1. Issue Operations
Create new issues, update existing ones, search with filters, and manage issue lifecycle.

### 2. Project Management
Create and list projects, organize issues into projects, and track project progress.

### 3. Team Workflow
Access team information, workflow states, labels, and member details.

### 4. Collaboration
Add comments to issues, track discussions, and coordinate with team members.

## Available Tools

### `linear_create_issue()`

Create a new issue in Linear.

**Required Parameters:**
- `title` (str) - Issue title
- `teamId` (str) - Team ID where the issue will be created

**Optional Parameters:**
- `description` (str) - Issue description with Markdown support
- `priority` (int) - Priority level (0=none, 1=urgent, 2=high, 3=medium, 4=low)
- `status` (str) - Initial status/state ID
- `assigneeId` (str) - User ID to assign the issue to
- `projectId` (str) - Project ID to associate with
- `labels` (list) - Array of label IDs

**Returns:** Created issue object with ID, identifier, and URL

**Example:**
```python
# Create a basic issue
issue = linear_create_issue(
    title="Fix login bug",
    teamId="team-id-here"
)

# Create issue with all details
issue = linear_create_issue(
    title="Implement user authentication",
    teamId="team-id",
    description="Add JWT-based authentication to the API",
    priority=2,
    assigneeId="user-id",
    projectId="project-id",
    labels=["bug-id", "urgent-id"]
)
```

### `linear_update_issue()`

Update an existing Linear issue.

**Required Parameters:**
- `id` (str) - Issue ID to update

**Optional Parameters:**
- `title` (str) - New issue title
- `description` (str) - New description
- `priority` (int) - New priority level (0-4)
- `status` (str) - New status/state ID
- `assigneeId` (str) - New assignee user ID

**Returns:** Updated issue object

**Example:**
```python
# Update issue status
issue = linear_update_issue(
    id="issue-id",
    status="in-progress-state-id"
)

# Update multiple fields
issue = linear_update_issue(
    id="issue-id",
    title="Updated title",
    priority=1,
    assigneeId="new-assignee-id"
)
```

### `linear_search_issues()`

Search and filter issues across your workspace.

**Optional Parameters:**
- `query` (str) - Text search in title/description
- `teamId` (str) - Filter by team ID
- `status` (str) - Filter by status/state ID
- `assigneeId` (str) - Filter by assignee user ID
- `labels` (list) - Filter by label IDs
- `priority` (int) - Filter by priority level
- `limit` (int) - Maximum number of results (default: 10)

**Returns:** List of matching issues

**Example:**
```python
# Search by text
results = linear_search_issues(query="authentication")

# Filter by team and status
results = linear_search_issues(
    teamId="team-id",
    status="in-progress-id",
    limit=20
)

# Find high priority bugs
results = linear_search_issues(
    priority=2,
    labels=["bug-label-id"]
)
```

### `linear_get_issue()`

Get a specific issue by ID or identifier.

**Required Parameters:**
- `id` (str) - Issue ID or identifier (e.g., "ENG-123")

**Returns:** Complete issue object with comments and details

**Example:**
```python
# Get by identifier
issue = linear_get_issue(id="ENG-123")

# Get by UUID
issue = linear_get_issue(id="issue-uuid-here")
```

### `linear_get_user_issues()`

Get issues assigned to a specific user.

**Optional Parameters:**
- `userId` (str) - User ID (omit for current authenticated user)
- `includeArchived` (bool) - Include archived/completed issues
- `limit` (int) - Maximum results (default: 50)

**Returns:** List of assigned issues

**Example:**
```python
# Get your assigned issues
my_issues = linear_get_user_issues()

# Get another user's issues
user_issues = linear_get_user_issues(userId="user-id")

# Include completed issues
all_issues = linear_get_user_issues(
    userId="user-id",
    includeArchived=True
)
```

### `linear_add_comment()`

Add a comment to an issue.

**Required Parameters:**
- `issueId` (str) - Issue ID to comment on
- `body` (str) - Comment text (supports Markdown)

**Returns:** Created comment object

**Example:**
```python
# Add a simple comment
comment = linear_add_comment(
    issueId="issue-id",
    body="This looks good to me!"
)

# Add formatted comment
comment = linear_add_comment(
    issueId="issue-id",
    body="## Code Review\n\n- ✅ Tests pass\n- ✅ Documentation updated"
)
```

### `linear_create_project()`

Create a new project in Linear.

**Required Parameters:**
- `name` (str) - Project name
- `teamId` (str) - Team ID for the project

**Optional Parameters:**
- `description` (str) - Project description
- `state` (str) - Project state (planned, started, completed, canceled)
- `targetDate` (str) - Target completion date (ISO 8601 format)

**Returns:** Created project object

**Example:**
```python
# Create a basic project
project = linear_create_project(
    name="Q1 Feature Launch",
    teamId="team-id"
)

# Create with full details
project = linear_create_project(
    name="API Migration",
    teamId="team-id",
    description="Migrate to REST API v2",
    state="started",
    targetDate="2025-12-31"
)
```

### `linear_list_projects()`

List all projects with optional filtering.

**Optional Parameters:**
- `teamId` (str) - Filter by team ID
- `state` (str) - Filter by state (planned, started, completed, canceled)

**Returns:** List of projects

**Example:**
```python
# Get all projects
projects = linear_list_projects()

# Get active projects for a team
projects = linear_list_projects(
    teamId="team-id",
    state="started"
)
```

### `linear_get_team()`

Get team information including workflow states and labels.

**Required Parameters:**
- `teamId` (str) - Team ID

**Returns:** Team object with states, labels, and members

**Example:**
```python
team = linear_get_team(teamId="team-id")

# Access workflow states
for state in team["states"]["nodes"]:
    print(f"{state['name']}: {state['type']}")
```

### `linear_list_teams()`

List all teams in your workspace.

**Returns:** List of teams

**Example:**
```python
teams = linear_list_teams()

for team in teams["teams"]["nodes"]:
    print(f"{team['key']}: {team['name']}")
```

## Setup and Authentication

### Prerequisites

1. **Linear Account** - You need access to a Linear workspace
2. **API Key** - Generate a Personal API key from Linear settings
3. **Team Access** - Ensure you have access to the teams you want to manage

### Configuration

1. **Generate API Key:**
   - Go to Linear Settings → API → Personal API keys
   - Click "Create new key"
   - Give it a descriptive name
   - Copy the generated key

2. **Set environment variable:**
```bash
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxxxxxxxxxxxxx"
```

3. **Verify access:**
```python
# Test by listing your teams
teams = linear_list_teams()
```

### Required Scopes / Permissions

Linear API keys have the same permissions as your user account:

- **read** - View issues, projects, and teams
- **write** - Create and update issues and projects
- **admin** - Full access (only if you're a workspace admin)

## Common Workflows

### Create and Track Issues

```python
# Get team ID
teams = linear_list_teams()
team_id = teams["teams"]["nodes"][0]["id"]

# Create issue
issue = linear_create_issue(
    title="Implement feature X",
    teamId=team_id,
    description="Detailed requirements...",
    priority=2
)

print(f"Created: {issue['issueCreate']['issue']['url']}")

# Track progress with comments
linear_add_comment(
    issueId=issue["issueCreate"]["issue"]["id"],
    body="Started implementation"
)
```

### Bulk Update Issues

```python
# Find all bugs
bugs = linear_search_issues(
    labels=["bug-label-id"],
    status="triage-state-id",
    limit=50
)

# Update priority
for issue in bugs["issues"]["nodes"]:
    linear_update_issue(
        id=issue["id"],
        priority=1  # Set to urgent
    )
```

### Project Setup Workflow

```python
# Get team info to see available states
team = linear_get_team(teamId="team-id")

# Create project
project = linear_create_project(
    name="Q2 Goals",
    teamId="team-id",
    targetDate="2025-06-30"
)

# Create milestone issues
for milestone in ["Planning", "Development", "Testing", "Launch"]:
    linear_create_issue(
        title=milestone,
        teamId="team-id",
        projectId=project["projectCreate"]["project"]["id"],
        priority=2
    )
```

### Daily Standup Report

```python
# Get your issues
issues = linear_get_user_issues(limit=20)

print("## My Current Issues\n")
for issue in issues["issues"]["nodes"]:
    print(f"- [{issue['identifier']}] {issue['title']}")
    print(f"  Status: {issue['state']['name']}")
    print(f"  Priority: {issue['priority']}\n")
```

## Implementation Notes

- **GraphQL API** - Linear uses GraphQL, so all requests are POST to a single endpoint
- **State IDs** - Status/state is referenced by ID, not name; use `linear_get_team()` to see available states
- **Identifiers** - Issues can be accessed by UUID or human-readable identifier (e.g., "ENG-123")
- **Pagination** - Results are limited by the `limit` parameter; use GraphQL cursors for large datasets
- **Markdown** - Descriptions and comments support full Markdown formatting

## Error Handling

Common error scenarios and solutions:

- **Authentication failed:** Verify `LINEAR_API_KEY` is set and valid
- **Team not found:** Check team ID is correct; use `linear_list_teams()` to find valid IDs
- **State not found:** State IDs are team-specific; use `linear_get_team()` to get valid state IDs
- **Issue not found:** Verify issue ID or identifier is correct
- **Rate limit:** Linear has rate limits; add delays between bulk operations
- **GraphQL errors:** Check the `errors` field in responses for detailed error messages

## Security Best Practices

1. **API key security** - Store `LINEAR_API_KEY` securely, never commit to version control
2. **Minimal permissions** - Use accounts with appropriate access levels
3. **Key rotation** - Regularly rotate API keys from Linear settings
4. **Audit access** - Review API key usage in Linear settings
5. **Read-only keys** - For reporting/dashboards, consider using read-only accounts

## Cost Considerations

**IMPORTANT:** Linear API has rate limits to ensure service quality.

### Rate Limits

Linear enforces the following rate limits:

- **1,200 requests per hour** - Per API key
- **60 requests per minute** - Burst protection
- **Complexity-based limits** - Complex GraphQL queries count more

**Best practices:**
- Cache team/project data to reduce repeated queries
- Use batch operations when possible
- Implement exponential backoff for rate limit errors
- Monitor your usage in Linear settings

### Linear Plans

- **Free Plan:** API access with standard rate limits
- **Standard/Plus:** Same API access with standard limits
- **Enterprise:** May have higher rate limits (contact Linear)

**Note:** API access is available on all Linear plans with the same rate limits.
