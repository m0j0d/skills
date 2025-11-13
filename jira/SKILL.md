---
name: atlassian-jira
description: Comprehensive Atlassian Jira Cloud integration enabling project management, issue tracking, workflow automation, and development information retrieval through natural language commands. Manage projects, create and update issues, search with JQL, add comments, and track development activity.
license: MIT
---

# Atlassian Jira Integration

Professional Jira Cloud integration that brings complete project management and issue tracking capabilities to AI assistants.

**Note:** Implements Jira Cloud REST API v3 directly

## When to Use This Skill

Use this skill when you need to:
- **Manage Projects**: List, search, and get detailed information about Jira projects
- **Track Issues**: Search, view, create, and update issues using natural language or JQL
- **Workflow Management**: Check available statuses, get transitions, and move issues through workflows
- **Team Collaboration**: Add comments, assign issues, set priorities
- **Development Tracking**: View commits, pull requests, and branches linked to issues
- **Reporting & Analytics**: Search and analyze issues across projects

## Available Tools

### Project Management

#### `list_projects`
List all Jira projects you have access to, with optional search filtering.

**Parameters:**
- `search` (optional): Filter projects by name or key

**Example Usage:**
```python
python scripts/jira_tools.py list-projects
python scripts/jira_tools.py list-projects --search "Platform"
```

#### `get_project`
Get detailed information about a specific project including description, lead, issue types, and components.

**Parameters:**
- `project_key_or_id` (required): Project key (e.g., "PROJ") or ID

**Example Usage:**
```python
python scripts/jira_tools.py get-project PROJ
```

### Issue Operations

#### `search_issues`
Search for issues using JQL (Jira Query Language) or simple filters. Supports complex queries for advanced filtering.

**Parameters:**
- `jql` (optional): JQL query string
- `project_key_or_id` (optional): Limit search to specific project
- `max_results` (optional): Maximum results to return (default: 50)

**Example Usage:**
```python
# Search by project
python scripts/jira_tools.py search-issues --project PROJ

# Search with JQL
python scripts/jira_tools.py search-issues --jql "project=PROJ AND status='In Progress'"

# Find high priority bugs
python scripts/jira_tools.py search-issues --jql "priority=High AND type=Bug"
```

**Common JQL Patterns:**
- Find my issues: `assignee = currentUser()`
- Open bugs: `type = Bug AND status = Open`
- Recent updates: `updated >= -7d ORDER BY updated DESC`
- Sprint issues: `sprint = "Sprint 23" AND status != Done`

#### `get_issue`
Retrieve complete details about an issue including description, comments, attachments, transitions, and change history.

**Parameters:**
- `issue_key_or_id` (required): Issue key (e.g., "PROJ-123") or ID

**Example Usage:**
```python
python scripts/jira_tools.py get-issue PROJ-123
```

#### `create_issue`
Create a new Jira issue with specified fields and properties.

**Parameters:**
- `project_key_or_id` (required): Project key or ID
- `summary` (required): Issue title/summary
- `issue_type` (required): Type (Bug, Story, Task, Epic, etc.)
- `description` (optional): Detailed description
- `priority` (optional): Priority level (Highest, High, Medium, Low, Lowest)
- `assignee` (optional): Assignee account ID or username

**Example Usage:**
```python
python scripts/jira_tools.py create-issue PROJ "Fix login bug" Bug \
  --description "Users cannot log in with SSO" \
  --priority High \
  --assignee john.doe
```

#### `update_issue`
Update fields on an existing issue.

**Parameters:**
- `issue_key_or_id` (required): Issue key or ID
- `fields` (required): Dictionary of fields to update

**Note:** This tool is primarily used programmatically. For CLI usage, consider using `add_comment` or creating a new issue.

#### `add_comment`
Add a comment to an existing issue for collaboration and updates.

**Parameters:**
- `issue_key_or_id` (required): Issue key or ID
- `body` (required): Comment text

**Example Usage:**
```python
python scripts/jira_tools.py add-comment PROJ-123 "Code review completed, ready for testing"
```

### Development Integration

#### `get_dev_info`
Retrieve development information linked to an issue, including commits, pull requests, and branches from connected development tools.

**Parameters:**
- `issue_key_or_id` (required): Issue key or ID

**Example Usage:**
```python
python scripts/jira_tools.py get-dev-info PROJ-123
```

**Returns:**
- Commits associated with the issue
- Pull requests and their status
- Branch information
- Build and deployment data (if integrated)

### Workflow Management

#### `list_statuses`
Get all available workflow statuses for a project, useful for understanding possible issue states.

**Parameters:**
- `project_key_or_id` (required): Project key or ID

**Example Usage:**
```python
python scripts/jira_tools.py list-statuses PROJ
```

#### `get_transitions`
Get available workflow transitions for a specific issue. Each issue can only transition to certain statuses based on your workflow configuration.

**Parameters:**
- `issue_key_or_id` (required): Issue key or ID

**Example Usage:**
```python
python scripts/jira_tools.py get-transitions PROJ-123
```

**Returns:**
- List of available transitions with IDs and names
- Transition IDs needed for `transition_issue`

**Example Output:**
```json
[
  {
    "id": "11",
    "name": "To Do",
    "to": {
      "id": "10000",
      "name": "To Do"
    }
  },
  {
    "id": "21",
    "name": "In Progress",
    "to": {
      "id": "10001",
      "name": "In Progress"
    }
  },
  {
    "id": "31",
    "name": "Done",
    "to": {
      "id": "10002",
      "name": "Done"
    }
  }
]
```

#### `transition_issue`
Move an issue through your workflow by executing a transition. Use `get_transitions` first to see available transitions and their IDs.

**Parameters:**
- `issue_key_or_id` (required): Issue key or ID
- `transition_id` (required): Transition ID from `get_transitions`

**Example Usage:**
```python
# First, get available transitions
python scripts/jira_tools.py get-transitions PROJ-123

# Then transition using the ID
python scripts/jira_tools.py transition-issue PROJ-123 21
```

**Common Workflow:**
1. Get issue details to see current status
2. Get available transitions for that issue
3. Choose desired transition ID
4. Execute transition

**Note:** Available transitions depend on:
- Issue's current status
- Your workflow configuration
- Your permissions on the issue

## Setup & Configuration

### Prerequisites

1. **Jira Cloud Account** with appropriate permissions
2. **API Token** from Atlassian

### Obtaining API Token

1. Visit [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a descriptive name (e.g., "AI Assistant")
4. Copy the token immediately (you won't see it again)

### Environment Variables

Set the following environment variables before using the skill:

```bash
export ATLASSIAN_SITE_NAME="mycompany"  # For mycompany.atlassian.net
export ATLASSIAN_USER_EMAIL="your.email@company.com"
export ATLASSIAN_API_TOKEN="your_api_token_here"
```

### Installation

Install required dependencies:

```bash
pip install requests --break-system-packages
```

### Validation

After setting up environment variables and dependencies, validate your configuration:

```bash
# From project root
npm run validate:jira

# Or directly
python skills/jira/scripts/validate.py
```

The validation script checks:
- **Environment variables** - All required credentials are set
- **Python dependencies** - Required libraries are installed
- **API connectivity** - Basic connection to Jira Cloud works

All checks must pass before using the skill. If validation fails, follow the error messages to fix configuration issues.

## Common Workflows

### Daily Standup Preparation
```bash
# Find my issues in progress
python scripts/jira_tools.py search-issues --jql "assignee=currentUser() AND status='In Progress'"

# Check recently updated issues
python scripts/jira_tools.py search-issues --jql "assignee=currentUser() AND updated >= -1d"
```

### Bug Triage
```bash
# List all open bugs
python scripts/jira_tools.py search-issues --jql "type=Bug AND status=Open ORDER BY priority DESC"

# Get details on high-priority bug
python scripts/jira_tools.py get-issue PROJ-456

# Add triage comment
python scripts/jira_tools.py add-comment PROJ-456 "Confirmed bug, reproduces in production"
```

### Sprint Planning
```bash
# Find unassigned stories
python scripts/jira_tools.py search-issues --jql "type=Story AND assignee IS EMPTY"

# Create new task
python scripts/jira_tools.py create-issue PROJ "Implement user authentication" Task \
  --description "Add OAuth 2.0 support" \
  --priority High
```

### Release Management
```bash
# Find issues in current release
python scripts/jira_tools.py search-issues --jql "fixVersion='Release 2.0' AND status!=Done"

# Check development status
python scripts/jira_tools.py get-dev-info PROJ-789
```

### Workflow Transition
```bash
# Check current status
python scripts/jira_tools.py get-issue PROJ-123

# See what transitions are available
python scripts/jira_tools.py get-transitions PROJ-123

# Move to "In Progress"
python scripts/jira_tools.py transition-issue PROJ-123 21

# Verify transition
python scripts/jira_tools.py get-issue PROJ-123
```

## Implementation Notes

### Authentication
- Uses Jira Cloud REST API v3
- Basic authentication with email + API token
- Token is base64-encoded for security
- All requests use HTTPS

### API Compatibility
- **Jira Cloud**: Fully supported ✓
- **Jira Server/Data Center**: Not supported (requires different auth)

### Rate Limiting
Jira Cloud enforces rate limits. The skill respects these limits:
- Free tier: ~200 requests/minute
- Standard tier: ~500 requests/minute
- Premium tier: ~1000 requests/minute

### Data Format
- Issues use Atlassian Document Format (ADF) for rich text
- Search results include essential fields for performance
- Full issue details available via `get_issue`

## Troubleshooting

### "Authentication failed"
- Verify your API token is correct and hasn't expired
- Ensure email address matches your Atlassian account
- Check that site name is correct (without .atlassian.net)

### "Permission denied"
- Confirm you have access to the project in Jira
- Check project permissions in Jira settings
- Verify issue-level security isn't restricting access

### "Issue type not found"
- Use exact issue type names from your Jira instance
- Common types: Bug, Story, Task, Epic, Sub-task
- Get available types: `python scripts/jira_tools.py get-project PROJ`

### "JQL syntax error"
- Validate JQL in Jira's issue search first
- Use quotes for multi-word values: `status = "In Progress"`
- Reference: [JQL Documentation](https://www.atlassian.com/software/jira/guides/expand-jira/jql)

## Bundled Scripts

- **`scripts/jira_tools.py`** - Main implementation with all Jira tools
  - Complete Jira REST API v3 client
  - CLI interface for all operations
  - Error handling and validation

## Advanced Usage

### Programmatic Access

```python
from scripts.jira_tools import JiraClient

# Initialize client
client = JiraClient(
    site_name="mycompany",
    user_email="user@company.com",
    api_token="your_token"
)

# Search for issues
issues = client.search_issues(jql="project=PROJ AND status=Open")

# Create issue
new_issue = client.create_issue(
    project_key_or_id="PROJ",
    summary="New feature request",
    issue_type="Story",
    description="Add dark mode support"
)

# Add comment
client.add_comment(new_issue['key'], "Starting work on this")
```

### Batch Operations

Process multiple issues efficiently:

```python
# Get all high-priority bugs
bugs = client.search_issues(
    jql="type=Bug AND priority=High",
    max_results=100
)

# Add comment to each
for bug in bugs:
    client.add_comment(
        bug['key'],
        "Scheduled for next sprint"
    )
```

## Best Practices

1. **Use JQL for Complex Queries**: JQL is more powerful than simple filters
2. **Limit Result Sets**: Use `max_results` to avoid overwhelming responses
3. **Cache Project Info**: Project details don't change often
4. **Batch Similar Operations**: Group API calls when possible
5. **Follow Naming Conventions**: Use consistent issue naming in your org

## Security Considerations

- **Never commit API tokens** to version control
- **Use environment variables** for credentials
- **Rotate tokens regularly** (every 90 days recommended)
- **Limit token permissions** to only what's needed
- **Monitor token usage** in Atlassian admin console

## Related Resources

- [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [JQL (Jira Query Language) Guide](https://www.atlassian.com/software/jira/guides/expand-jira/jql)
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Jira Automation](https://www.atlassian.com/software/jira/features/automation)

## Skill Origin

This skill provides similar functionality to open-source Jira MCP servers, implemented independently using Atlassian's Jira Cloud REST API v3 documentation. It offers local execution without requiring an MCP server connection.

**Similar open-source implementations:**
- `sooperset/mcp-atlassian` (MIT License, 3.5k stars) - Python MCP server for Atlassian tools
- `phuc-nt/mcp-atlassian-server` (MIT License) - TypeScript MCP server for Jira & Confluence
- `@aashari/mcp-server-atlassian-jira` (ISC License) - Node.js/TypeScript MCP server for Jira

This implementation is built from the official Atlassian Jira Cloud REST API v3 documentation and does not derive from the above codebases.
