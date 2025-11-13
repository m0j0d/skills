#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
GitHub Integration Tools

Provides issue, PR, and repository management via GitHub REST API.
"""

import os
import sys
import json
import requests
from typing import Optional, List, Dict, Any


def get_github_token():
    """Get GitHub token from environment"""
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
    return token


def make_request(method: str, url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated request to GitHub API"""
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json() if response.text else {}
    except requests.exceptions.HTTPError as e:
        error_msg = f"GitHub API error: {e}"
        if e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f"\n{json.dumps(error_detail, indent=2)}"
            except:
                error_msg += f"\n{e.response.text}"
        raise Exception(error_msg)
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


# ============================================================================
# ISSUE MANAGEMENT
# ============================================================================

def list_issues(owner: str, repo: str, state: str = "open", labels: str = "",
                assignee: str = "", sort: str = "created", direction: str = "desc",
                per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List repository issues

    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state (open, closed, all)
        labels: Comma-separated label names
        assignee: Filter by assignee username
        sort: Sort by (created, updated, comments)
        direction: Sort direction (asc, desc)
        per_page: Results per page (max 100)
        page: Page number
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page
    }

    if labels:
        params["labels"] = labels
    if assignee:
        params["assignee"] = assignee

    return make_request("GET", url, params)


def issue_read(owner: str, repo: str, issue_number: int) -> Dict:
    """
    Get detailed issue information

    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    issue = make_request("GET", url)

    # Get comments
    comments_url = issue["comments_url"]
    comments = make_request("GET", comments_url)
    issue["comment_list"] = comments

    return issue


def issue_write(owner: str, repo: str, title: str, body: str = "",
                labels: Optional[List[str]] = None, assignees: Optional[List[str]] = None,
                issue_number: Optional[int] = None, state: Optional[str] = None) -> Dict:
    """
    Create or update an issue

    Args:
        owner: Repository owner
        repo: Repository name
        title: Issue title
        body: Issue description
        labels: List of label names
        assignees: List of assignee usernames
        issue_number: If provided, update existing issue
        state: Issue state (open, closed) - for updates only
    """
    data = {"title": title}

    if body:
        data["body"] = body
    if labels:
        data["labels"] = labels
    if assignees:
        data["assignees"] = assignees
    if state:
        data["state"] = state

    if issue_number:
        # Update existing issue
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        return make_request("PATCH", url, data)
    else:
        # Create new issue
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        return make_request("POST", url, data)


def add_issue_comment(owner: str, repo: str, issue_number: int, body: str) -> Dict:
    """
    Add comment to an issue

    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        body: Comment text
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    data = {"body": body}
    return make_request("POST", url, data)


def search_issues(query: str, sort: str = "created", order: str = "desc",
                  per_page: int = 30, page: int = 1) -> Dict:
    """
    Search issues across repositories

    Args:
        query: GitHub search query (e.g., "repo:owner/repo is:issue is:open")
        sort: Sort by (comments, created, updated)
        order: Sort order (asc, desc)
        per_page: Results per page (max 100)
        page: Page number
    """
    url = "https://api.github.com/search/issues"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": per_page,
        "page": page
    }
    return make_request("GET", url, params)


# ============================================================================
# PULL REQUEST MANAGEMENT
# ============================================================================

def list_pull_requests(owner: str, repo: str, state: str = "open",
                       head: str = "", base: str = "", sort: str = "created",
                       direction: str = "desc", per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List repository pull requests

    Args:
        owner: Repository owner
        repo: Repository name
        state: PR state (open, closed, all)
        head: Filter by head branch
        base: Filter by base branch
        sort: Sort by (created, updated, popularity, long-running)
        direction: Sort direction (asc, desc)
        per_page: Results per page (max 100)
        page: Page number
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {
        "state": state,
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page
    }

    if head:
        params["head"] = head
    if base:
        params["base"] = base

    return make_request("GET", url, params)


def pull_request_read(owner: str, repo: str, pr_number: int) -> Dict:
    """
    Get detailed pull request information

    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: PR number
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    pr = make_request("GET", url)

    # Get files changed
    files_url = f"{url}/files"
    files = make_request("GET", files_url)
    pr["files_changed"] = files

    # Get reviews
    reviews_url = f"{url}/reviews"
    reviews = make_request("GET", reviews_url)
    pr["reviews"] = reviews

    # Get comments
    comments_url = pr["comments_url"]
    comments = make_request("GET", comments_url)
    pr["comment_list"] = comments

    return pr


def create_pull_request(owner: str, repo: str, title: str, head: str, base: str,
                        body: str = "", draft: bool = False) -> Dict:
    """
    Create a new pull request

    Args:
        owner: Repository owner
        repo: Repository name
        title: PR title
        head: Head branch (source)
        base: Base branch (target)
        body: PR description
        draft: Create as draft PR
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body,
        "draft": draft
    }
    return make_request("POST", url, data)


def update_pull_request(owner: str, repo: str, pr_number: int,
                        title: Optional[str] = None, body: Optional[str] = None,
                        state: Optional[str] = None, base: Optional[str] = None) -> Dict:
    """
    Update pull request details

    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: PR number
        title: New title
        body: New description
        state: New state (open, closed)
        base: New base branch
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    data = {}

    if title is not None:
        data["title"] = title
    if body is not None:
        data["body"] = body
    if state is not None:
        data["state"] = state
    if base is not None:
        data["base"] = base

    return make_request("PATCH", url, data)


def merge_pull_request(owner: str, repo: str, pr_number: int,
                       merge_method: str = "merge", commit_title: str = "",
                       commit_message: str = "") -> Dict:
    """
    Merge a pull request

    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: PR number
        merge_method: Merge method (merge, squash, rebase)
        commit_title: Custom commit title
        commit_message: Custom commit message
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    data = {"merge_method": merge_method}

    if commit_title:
        data["commit_title"] = commit_title
    if commit_message:
        data["commit_message"] = commit_message

    return make_request("PUT", url, data)


# ============================================================================
# REPOSITORY OPERATIONS
# ============================================================================

def get_repo(owner: str, repo: str) -> Dict:
    """
    Get repository information

    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    return make_request("GET", url)


def search_repos(query: str, sort: str = "stars", order: str = "desc",
                 per_page: int = 30, page: int = 1) -> Dict:
    """
    Search for repositories

    Args:
        query: Search query (e.g., "language:python stars:>1000")
        sort: Sort by (stars, forks, help-wanted-issues, updated)
        order: Sort order (asc, desc)
        per_page: Results per page (max 100)
        page: Page number
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": per_page,
        "page": page
    }
    return make_request("GET", url, params)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: github_tools.py <command> [args...]")
        print("\nCommands:")
        print("  list-issues <owner> <repo> [--state open|closed|all]")
        print("  get-issue <owner> <repo> <issue_number>")
        print("  create-issue <owner> <repo> <title> [body]")
        print("  update-issue <owner> <repo> <issue_number> <title> [body]")
        print("  add-comment <owner> <repo> <issue_number> <body>")
        print("  search-issues <query>")
        print("  list-prs <owner> <repo> [--state open|closed|all]")
        print("  get-pr <owner> <repo> <pr_number>")
        print("  create-pr <owner> <repo> <title> <head> <base> [body]")
        print("  update-pr <owner> <repo> <pr_number> <title> [body]")
        print("  merge-pr <owner> <repo> <pr_number> [--method merge|squash|rebase]")
        print("  get-repo <owner> <repo>")
        print("  search-repos <query>")
        return

    command = sys.argv[1]

    try:
        if command == "list-issues":
            owner, repo = sys.argv[2], sys.argv[3]
            state = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4].startswith("--state") else "open"
            if state.startswith("--state="):
                state = state.split("=")[1]
            result = list_issues(owner, repo, state=state)
            print(json.dumps(result, indent=2))

        elif command == "get-issue":
            owner, repo, issue_number = sys.argv[2], sys.argv[3], int(sys.argv[4])
            result = issue_read(owner, repo, issue_number)
            print(json.dumps(result, indent=2))

        elif command == "create-issue":
            owner, repo, title = sys.argv[2], sys.argv[3], sys.argv[4]
            body = sys.argv[5] if len(sys.argv) > 5 else ""
            result = issue_write(owner, repo, title, body)
            print(json.dumps(result, indent=2))

        elif command == "update-issue":
            owner, repo, issue_number, title = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
            body = sys.argv[6] if len(sys.argv) > 6 else ""
            result = issue_write(owner, repo, title, body, issue_number=issue_number)
            print(json.dumps(result, indent=2))

        elif command == "add-comment":
            owner, repo, issue_number, body = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
            result = add_issue_comment(owner, repo, issue_number, body)
            print(json.dumps(result, indent=2))

        elif command == "search-issues":
            query = sys.argv[2]
            result = search_issues(query)
            print(json.dumps(result, indent=2))

        elif command == "list-prs":
            owner, repo = sys.argv[2], sys.argv[3]
            state = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4].startswith("--state") else "open"
            if state.startswith("--state="):
                state = state.split("=")[1]
            result = list_pull_requests(owner, repo, state=state)
            print(json.dumps(result, indent=2))

        elif command == "get-pr":
            owner, repo, pr_number = sys.argv[2], sys.argv[3], int(sys.argv[4])
            result = pull_request_read(owner, repo, pr_number)
            print(json.dumps(result, indent=2))

        elif command == "create-pr":
            owner, repo, title, head, base = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
            body = sys.argv[7] if len(sys.argv) > 7 else ""
            result = create_pull_request(owner, repo, title, head, base, body)
            print(json.dumps(result, indent=2))

        elif command == "update-pr":
            owner, repo, pr_number, title = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
            body = sys.argv[6] if len(sys.argv) > 6 else ""
            result = update_pull_request(owner, repo, pr_number, title=title, body=body)
            print(json.dumps(result, indent=2))

        elif command == "merge-pr":
            owner, repo, pr_number = sys.argv[2], sys.argv[3], int(sys.argv[4])
            method = "merge"
            if len(sys.argv) > 5 and sys.argv[5].startswith("--method"):
                method = sys.argv[5].split("=")[1] if "=" in sys.argv[5] else sys.argv[6]
            result = merge_pull_request(owner, repo, pr_number, merge_method=method)
            print(json.dumps(result, indent=2))

        elif command == "get-repo":
            owner, repo = sys.argv[2], sys.argv[3]
            result = get_repo(owner, repo)
            print(json.dumps(result, indent=2))

        elif command == "search-repos":
            query = sys.argv[2]
            result = search_repos(query)
            print(json.dumps(result, indent=2))

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
