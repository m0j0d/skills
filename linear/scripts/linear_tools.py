#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Wrapper functions for linear MCP server tools.
Auto-generated from MCP server specification.

This module provides Python functions that replicate the functionality
of the linear MCP server, allowing it to be used as a skill without
requiring the original MCP server connection.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
import requests


# Linear API configuration
LINEAR_API_BASE = "https://api.linear.app/graphql"


def _get_headers() -> Dict[str, str]:
    """Get headers for Linear GraphQL API requests."""
    api_key = os.getenv("LINEAR_API_KEY")
    if not api_key:
        raise ValueError("LINEAR_API_KEY environment variable not set")

    return {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }


def _make_request(query: str, variables: Dict = None) -> Dict[str, Any]:
    """Make a GraphQL request to the Linear API."""
    headers = _get_headers()
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = requests.post(LINEAR_API_BASE, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            return {
                "error": True,
                "message": "GraphQL errors",
                "details": result["errors"]
            }

        return result.get("data", {})
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


def linear_create_issue(title: str, teamId: str, description: str = '', priority: int = 0, status: str = '', assigneeId: str = '', projectId: str = '', labels: List = None) -> Dict[str, Any]:
    """
    Create a new Linear issue

    Args:
        title: Issue title
        teamId: Team ID where issue will be created
        description: Issue description (supports Markdown)
        priority: Priority level (0=none, 1=urgent, 2=high, 3=medium, 4=low)
        status: Initial status name
        assigneeId: User ID to assign issue to
        projectId: Project ID to associate with
        labels: Array of label IDs

    Returns:
        Created issue object
    """
    query = """
    mutation IssueCreate($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          id
          identifier
          title
          description
          priority
          state {
            id
            name
          }
          assignee {
            id
            name
          }
          team {
            id
            name
          }
          url
        }
      }
    }
    """

    input_data = {
        "title": title,
        "teamId": teamId
    }

    if description:
        input_data["description"] = description
    if priority > 0:
        input_data["priority"] = priority
    if status:
        input_data["stateId"] = status  # Note: Linear uses stateId, not status name
    if assigneeId:
        input_data["assigneeId"] = assigneeId
    if projectId:
        input_data["projectId"] = projectId
    if labels:
        input_data["labelIds"] = labels

    variables = {"input": input_data}
    return _make_request(query, variables)


def linear_update_issue(id: str, title: str = '', description: str = '', priority: int = None, status: str = '', assigneeId: str = '') -> Dict[str, Any]:
    """
    Update an existing Linear issue

    Args:
        id: Issue ID to update
        title: New title
        description: New description
        priority: New priority level (0-4)
        status: New status name
        assigneeId: New assignee user ID

    Returns:
        Updated issue object
    """
    query = """
    mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue {
          id
          identifier
          title
          description
          priority
          state {
            id
            name
          }
          assignee {
            id
            name
          }
        }
      }
    }
    """

    input_data = {}
    if title:
        input_data["title"] = title
    if description:
        input_data["description"] = description
    if priority is not None:
        input_data["priority"] = priority
    if status:
        input_data["stateId"] = status
    if assigneeId:
        input_data["assigneeId"] = assigneeId

    variables = {"id": id, "input": input_data}
    return _make_request(query, variables)


def linear_search_issues(query: str = '', teamId: str = '', status: str = '', assigneeId: str = '', labels: List = None, priority: int = None, limit: int = 10) -> Dict[str, Any]:
    """
    Search and filter Linear issues

    Args:
        query: Text search in title/description
        teamId: Filter by team ID
        status: Filter by status name
        assigneeId: Filter by assignee user ID
        labels: Filter by label IDs
        priority: Filter by priority level
        limit: Maximum number of results (default: 10)

    Returns:
        List of matching issues
    """
    graphql_query = """
    query Issues($filter: IssueFilter, $first: Int) {
      issues(filter: $filter, first: $first) {
        nodes {
          id
          identifier
          title
          description
          priority
          state {
            id
            name
          }
          assignee {
            id
            name
          }
          team {
            id
            name
          }
          labels {
            nodes {
              id
              name
            }
          }
          url
          createdAt
          updatedAt
        }
      }
    }
    """

    filter_data = {}
    if query:
        filter_data["title"] = {"contains": query}
    if teamId:
        filter_data["team"] = {"id": {"eq": teamId}}
    if status:
        filter_data["state"] = {"id": {"eq": status}}
    if assigneeId:
        filter_data["assignee"] = {"id": {"eq": assigneeId}}
    if labels:
        filter_data["labels"] = {"id": {"in": labels}}
    if priority is not None:
        filter_data["priority"] = {"eq": priority}

    variables = {"first": limit}
    if filter_data:
        variables["filter"] = filter_data

    return _make_request(graphql_query, variables)


def linear_get_issue(id: str) -> Dict[str, Any]:
    """
    Get a specific issue by ID or identifier

    Args:
        id: Issue ID or identifier (e.g., ENG-123)

    Returns:
        Issue object
    """
    query = """
    query Issue($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        priority
        state {
          id
          name
        }
        assignee {
          id
          name
        }
        team {
          id
          name
        }
        project {
          id
          name
        }
        labels {
          nodes {
            id
            name
          }
        }
        comments {
          nodes {
            id
            body
            user {
              id
              name
            }
            createdAt
          }
        }
        url
        createdAt
        updatedAt
      }
    }
    """

    variables = {"id": id}
    return _make_request(query, variables)


def linear_get_user_issues(userId: str = '', includeArchived: bool = False, limit: int = 50) -> Dict[str, Any]:
    """
    Get issues assigned to a user

    Args:
        userId: User ID (omit for current user)
        includeArchived: Include archived issues
        limit: Maximum results (default: 50)

    Returns:
        List of assigned issues
    """
    query = """
    query UserIssues($userId: String, $filter: IssueFilter, $first: Int) {
      issues(filter: $filter, first: $first) {
        nodes {
          id
          identifier
          title
          description
          priority
          state {
            id
            name
          }
          team {
            id
            name
          }
          url
          createdAt
          updatedAt
        }
      }
    }
    """

    filter_data = {}
    if userId:
        filter_data["assignee"] = {"id": {"eq": userId}}
    else:
        filter_data["assignee"] = {"isMe": {"eq": True}}

    if not includeArchived:
        filter_data["state"] = {"type": {"neq": "completed"}}

    variables = {"first": limit, "filter": filter_data}
    return _make_request(query, variables)


def linear_add_comment(issueId: str, body: str) -> Dict[str, Any]:
    """
    Add a comment to an issue

    Args:
        issueId: Issue ID to comment on
        body: Comment text (supports Markdown)

    Returns:
        Created comment object
    """
    query = """
    mutation CommentCreate($input: CommentCreateInput!) {
      commentCreate(input: $input) {
        success
        comment {
          id
          body
          user {
            id
            name
          }
          issue {
            id
            identifier
          }
          createdAt
        }
      }
    }
    """

    input_data = {
        "issueId": issueId,
        "body": body
    }

    variables = {"input": input_data}
    return _make_request(query, variables)


def linear_create_project(name: str, teamId: str, description: str = '', state: str = 'planned', targetDate: str = '') -> Dict[str, Any]:
    """
    Create a new Linear project

    Args:
        name: Project name
        teamId: Team ID for the project
        description: Project description
        state: Project state (planned, started, completed, canceled)
        targetDate: Target completion date (ISO 8601)

    Returns:
        Created project object
    """
    query = """
    mutation ProjectCreate($input: ProjectCreateInput!) {
      projectCreate(input: $input) {
        success
        project {
          id
          name
          description
          state
          targetDate
          team {
            id
            name
          }
          url
        }
      }
    }
    """

    input_data = {
        "name": name,
        "teamIds": [teamId]
    }

    if description:
        input_data["description"] = description
    if state:
        input_data["state"] = state
    if targetDate:
        input_data["targetDate"] = targetDate

    variables = {"input": input_data}
    return _make_request(query, variables)


def linear_list_projects(teamId: str = '', state: str = '') -> Dict[str, Any]:
    """
    List all projects with optional filtering

    Args:
        teamId: Filter by team ID
        state: Filter by state (planned, started, completed, canceled)

    Returns:
        List of projects
    """
    query = """
    query Projects($filter: ProjectFilter) {
      projects(filter: $filter) {
        nodes {
          id
          name
          description
          state
          targetDate
          teams {
            nodes {
              id
              name
            }
          }
          url
          createdAt
          updatedAt
        }
      }
    }
    """

    filter_data = {}
    if teamId:
        filter_data["teams"] = {"id": {"eq": teamId}}
    if state:
        filter_data["state"] = {"eq": state}

    variables = {}
    if filter_data:
        variables["filter"] = filter_data

    return _make_request(query, variables)


def linear_get_team(teamId: str) -> Dict[str, Any]:
    """
    Get team information including states and workflow

    Args:
        teamId: Team ID

    Returns:
        Team object with workflow details
    """
    query = """
    query Team($id: String!) {
      team(id: $id) {
        id
        name
        key
        description
        states {
          nodes {
            id
            name
            type
            color
          }
        }
        labels {
          nodes {
            id
            name
            color
          }
        }
        members {
          nodes {
            id
            name
          }
        }
      }
    }
    """

    variables = {"id": teamId}
    return _make_request(query, variables)


def linear_list_teams() -> Dict[str, Any]:
    """
    List all teams in the workspace

    Returns:
        List of teams
    """
    query = """
    query Teams {
      teams {
        nodes {
          id
          name
          key
          description
        }
      }
    }
    """

    return _make_request(query)


if __name__ == "__main__":
    """Command-line interface for tool execution."""

    if len(sys.argv) < 2:
        print("Usage: python linear_tools.py <tool_name> [--param value ...]")
        print("\nAvailable tools:")
        print("  linear_create_issue: Create a new Linear issue")
        print("  linear_update_issue: Update an existing Linear issue")
        print("  linear_search_issues: Search and filter Linear issues")
        print("  linear_get_issue: Get a specific issue by ID or identifier")
        print("  linear_get_user_issues: Get issues assigned to a user")
        print("  linear_add_comment: Add a comment to an issue")
        print("  linear_create_project: Create a new Linear project")
        print("  linear_list_projects: List all projects with optional filtering")
        print("  linear_get_team: Get team information including states and workflow")
        print("  linear_list_teams: List all teams in the workspace")
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
