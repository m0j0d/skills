---
name: github
description: GitHub repository management including issues, pull requests, comments, and repository operations for community management and development workflows
---

# GitHub Integration

Comprehensive GitHub repository management for issues, pull requests, and community workflows.

**Based on:** Anthropic's archived MCP server (@modelcontextprotocol/servers-archived)

## When to Use

- Create and manage issues
- Review and merge pull requests
- Add comments and labels
- Search issues and PRs
- Manage repositories
- Automate community workflows

## Setup

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token"
pip install requests --break-system-packages
```

### Token Permissions Required

Your GitHub Personal Access Token needs these scopes:
- `repo` - Full repository access
- `read:user` - Read user profile data
- `read:org` - Read organization membership (optional)

Create token at: https://github.com/settings/tokens

### Validation

After setup, validate your configuration:

```bash
# From project root
npm run validate:github

# Or directly
python integration-skills/github/scripts/validate.py
```

The validation script checks:
- **Environment variables** - GITHUB_PERSONAL_ACCESS_TOKEN is set
- **Python dependencies** - Required libraries are installed
- **API connectivity** - Token authentication and scopes are valid

All checks must pass before using the skill.

## Key Tools

### Issue Management

**list_issues** - List repository issues with filters
- Parameters: owner, repo, state (open/closed/all), labels, assignee

**issue_read** - Get detailed issue information
- Parameters: owner, repo, issue_number
- Returns: title, body, comments, labels, assignees

**issue_write** - Create or update issues
- Create: owner, repo, title, body, labels, assignees
- Update: owner, repo, issue_number, title, body, state

**add_issue_comment** - Comment on issues
- Parameters: owner, repo, issue_number, body

**search_issues** - Search issues across repositories
- Parameters: query (GitHub search syntax), sort, order

### Pull Request Management

**list_pull_requests** - List repository PRs
- Parameters: owner, repo, state (open/closed/all), head, base

**pull_request_read** - Get detailed PR information
- Parameters: owner, repo, pr_number
- Returns: title, body, diff, files, reviews, comments

**create_pull_request** - Open new pull request
- Parameters: owner, repo, title, body, head, base

**update_pull_request** - Update PR details
- Parameters: owner, repo, pr_number, title, body, state

**merge_pull_request** - Merge pull request
- Parameters: owner, repo, pr_number, merge_method (merge/squash/rebase)

### Repository Operations

**get_repo** - Get repository information
- Parameters: owner, repo
- Returns: description, stars, forks, language, topics

**search_repos** - Search for repositories
- Parameters: query (GitHub search syntax), sort, order

## Example Usage

```bash
# List open issues
python scripts/github_tools.py list-issues owner repo --state open

# Create new issue
python scripts/github_tools.py create-issue owner repo "Bug: Title" "Description"

# Comment on issue
python scripts/github_tools.py add-comment owner repo 123 "Thanks for reporting!"

# List pull requests
python scripts/github_tools.py list-prs owner repo --state open

# Get PR details
python scripts/github_tools.py get-pr owner repo 456

# Merge PR
python scripts/github_tools.py merge-pr owner repo 456 --method squash
```

## Common Workflows

### Triage New Issues
```python
# List new issues
issues = list_issues("owner", "repo", state="open", labels="", sort="created")

# Review each issue
for issue in issues[:10]:
    details = issue_read("owner", "repo", issue["number"])
    # Add labels, assign, or comment based on content
```

### Review and Merge PRs
```python
# List open PRs
prs = list_pull_requests("owner", "repo", state="open")

# Review PR
pr_details = pull_request_read("owner", "repo", pr_number)
# Check diff, files changed, tests

# Merge when ready
merge_pull_request("owner", "repo", pr_number, merge_method="squash")
```

### Monitor Community Activity
```python
# Search recent issues
recent = search_issues("repo:owner/repo is:issue created:>2025-10-20")

# Search specific topics
bugs = search_issues("repo:owner/repo is:issue label:bug is:open")
```

## Origin

Based on GitHub's official github-mcp-server.

## License

MIT - See LICENSE.txt in skill directory
