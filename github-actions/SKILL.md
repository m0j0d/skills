---
name: github-actions
description: GitHub Actions workflow management including triggering, monitoring, analyzing runs, and managing CI/CD pipelines directly from AI assistants
---

# GitHub Actions Integration

Comprehensive GitHub Actions workflow management for CI/CD automation.

**Note:** Original skill created from GitHub Actions API documentation

## When to Use

- List and trigger workflows
- Monitor workflow runs
- Analyze failed runs
- Cancel or rerun workflows
- Download workflow logs

## Setup

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token"
pip install requests --break-system-packages
```

### Validation

After setup, validate your configuration:

```bash
# From project root
npm run validate:github-actions

# Or directly
python skills/github-actions/scripts/validate.py
```

The validation script checks:
- **Environment variables** - GITHUB_PERSONAL_ACCESS_TOKEN is set
- **Python dependencies** - Required libraries are installed
- **API connectivity** - Token authentication and scopes are valid

All checks must pass before using the skill.

## Key Tools

**list_workflows** - List repository workflows
**trigger_workflow** - Start workflow with inputs
**list_workflow_runs** - View run history
**get_workflow_run** - Get run details
**cancel_workflow_run** - Cancel running workflow
**rerun_workflow** - Retry failed workflow
**get_workflow_logs** - Download logs

## Example Usage

```bash
# List workflows
python scripts/github_actions_tools.py list-workflows owner repo

# Trigger workflow
python scripts/github_actions_tools.py trigger owner repo ci.yml main

# Get run status
python scripts/github_actions_tools.py get-run owner repo 123456

# Cancel run
python scripts/github_actions_tools.py cancel owner repo 123456
```

## Origin

Based on GitHub's official github-mcp-server and ko1ynnky/github-actions-mcp-server.
