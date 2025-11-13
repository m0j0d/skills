#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Jira Cloud API Integration Tools
Comprehensive wrapper for Atlassian Jira Cloud REST API v3
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, List, Any
from urllib.parse import urlencode
import base64

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests --break-system-packages")
    sys.exit(1)


class JiraClient:
    """Client for interacting with Jira Cloud REST API"""
    
    def __init__(self, site_name: str, user_email: str, api_token: str):
        """
        Initialize Jira client
        
        Args:
            site_name: Jira site name (e.g., 'mycompany' for mycompany.atlassian.net)
            user_email: User's email address
            api_token: API token from Atlassian
        """
        self.base_url = f"https://{site_name}.atlassian.net"
        self.api_url = f"{self.base_url}/rest/api/3"
        self.user_email = user_email
        self.api_token = api_token
        
        # Create authentication header
        auth_string = f"{user_email}:{api_token}"
        auth_bytes = auth_string.encode('ascii')
        base64_bytes = base64.b64encode(auth_bytes)
        base64_string = base64_bytes.decode('ascii')
        
        self.headers = {
            "Authorization": f"Basic {base64_string}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an API request with improved error handling"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code
            error_body = response.text[:500] if response.text else 'No response body'

            if status_code == 410:
                raise Exception(
                    f"410 Gone - Endpoint deprecated or unavailable\n"
                    f"URL: {url}\n"
                    f"Method: {method}\n"
                    f"Response: {error_body}"
                )
            elif status_code == 401:
                raise Exception(f"401 Unauthorized - Check API token and email\nURL: {url}")
            elif status_code == 403:
                raise Exception(f"403 Forbidden - Insufficient permissions\nURL: {url}")
            elif status_code == 404:
                raise Exception(f"404 Not Found - {endpoint}")
            else:
                raise Exception(f"{status_code} Error: {str(e)}\nURL: {url}\nResponse: {error_body}")
    
    def list_projects(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all projects accessible to the user
        
        Args:
            search: Optional search term to filter projects
        
        Returns:
            List of project dictionaries
        """
        params = {}
        if search:
            params['query'] = search
        
        response = self._request('GET', 'project/search', params=params)
        data = response.json()
        return data.get('values', [])
    
    def get_project(self, project_key_or_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific project
        
        Args:
            project_key_or_id: Project key (e.g., 'PROJ') or ID
        
        Returns:
            Project details dictionary
        """
        response = self._request('GET', f'project/{project_key_or_id}')
        return response.json()
    
    def search_issues(
        self,
        jql: Optional[str] = None,
        project_key_or_id: Optional[str] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for issues using JQL

        Args:
            jql: JQL query string
            project_key_or_id: Optional project to limit scope
            max_results: Maximum number of results

        Returns:
            List of issues
        """
        if not jql and project_key_or_id:
            jql = f"project = {project_key_or_id}"
        elif not jql:
            jql = "ORDER BY created DESC"

        # Use the new /search/jql endpoint (old /search endpoint was deprecated)
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "summary,status,assignee,priority,created,updated,issuetype"
        }

        response = self._request('GET', 'search/jql', params=params)
        data = response.json()
        return data.get('issues', [])
    
    def get_issue(self, issue_key_or_id: str) -> Dict[str, Any]:
        """
        Get detailed information about an issue
        
        Args:
            issue_key_or_id: Issue key (e.g., 'PROJ-123') or ID
        
        Returns:
            Issue details dictionary
        """
        params = {
            'expand': 'renderedFields,changelog,transitions,operations'
        }
        response = self._request('GET', f'issue/{issue_key_or_id}', params=params)
        return response.json()
    
    def create_issue(
        self,
        project_key_or_id: str,
        summary: str,
        issue_type: str,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new issue
        
        Args:
            project_key_or_id: Project key or ID
            summary: Issue title
            issue_type: Type of issue (Bug, Story, Task, etc.)
            description: Issue description
            priority: Priority level
            assignee: Assignee account ID or username
        
        Returns:
            Created issue dictionary
        """
        fields = {
            "project": {"key": project_key_or_id} if len(project_key_or_id) < 10 else {"id": project_key_or_id},
            "summary": summary,
            "issuetype": {"name": issue_type}
        }
        
        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            }
        
        if priority:
            fields["priority"] = {"name": priority}
        
        if assignee:
            fields["assignee"] = {"accountId": assignee} if assignee.startswith('5') else {"name": assignee}
        
        payload = {"fields": fields}
        response = self._request('POST', 'issue', json=payload)
        return response.json()
    
    def update_issue(self, issue_key_or_id: str, fields: Dict[str, Any]) -> None:
        """
        Update an existing issue
        
        Args:
            issue_key_or_id: Issue key or ID
            fields: Dictionary of fields to update
        """
        payload = {"fields": fields}
        self._request('PUT', f'issue/{issue_key_or_id}', json=payload)
    
    def add_comment(self, issue_key_or_id: str, body: str) -> Dict[str, Any]:
        """
        Add a comment to an issue
        
        Args:
            issue_key_or_id: Issue key or ID
            body: Comment text
        
        Returns:
            Created comment dictionary
        """
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": body
                            }
                        ]
                    }
                ]
            }
        }
        response = self._request('POST', f'issue/{issue_key_or_id}/comment', json=payload)
        return response.json()
    
    def get_dev_info(self, issue_key_or_id: str) -> Dict[str, Any]:
        """
        Get development information linked to an issue
        
        Args:
            issue_key_or_id: Issue key or ID
        
        Returns:
            Development information dictionary
        """
        # Get issue with dev info
        response = self._request('GET', f'issue/{issue_key_or_id}', params={'fields': 'development'})
        data = response.json()
        
        # Also try to get remote links which often contain dev info
        links_response = self._request('GET', f'issue/{issue_key_or_id}/remotelink')
        
        return {
            "development": data.get('fields', {}).get('development', {}),
            "remoteLinks": links_response.json()
        }
    
    def list_statuses(self, project_key_or_id: str) -> List[Dict[str, Any]]:
        """
        Get available statuses for a project

        Args:
            project_key_or_id: Project key or ID

        Returns:
            List of status dictionaries
        """
        response = self._request('GET', f'project/{project_key_or_id}/statuses')
        return response.json()

    def get_transitions(self, issue_key_or_id: str) -> List[Dict[str, Any]]:
        """
        Get available workflow transitions for an issue

        Args:
            issue_key_or_id: Issue key or ID

        Returns:
            List of available transitions with IDs and names
        """
        response = self._request('GET', f'issue/{issue_key_or_id}/transitions')
        data = response.json()
        return data.get('transitions', [])

    def transition_issue(self, issue_key_or_id: str, transition_id: str) -> None:
        """
        Transition an issue to a new status

        Args:
            issue_key_or_id: Issue key or ID
            transition_id: ID of the transition to execute
        """
        payload = {
            "transition": {
                "id": transition_id
            }
        }
        self._request('POST', f'issue/{issue_key_or_id}/transitions', json=payload)


def get_client_from_env() -> JiraClient:
    """Get Jira client from environment variables"""
    site_name = os.environ.get('ATLASSIAN_SITE_NAME')
    user_email = os.environ.get('ATLASSIAN_USER_EMAIL')
    api_token = os.environ.get('ATLASSIAN_API_TOKEN')
    
    if not all([site_name, user_email, api_token]):
        raise ValueError(
            "Missing required environment variables: "
            "ATLASSIAN_SITE_NAME, ATLASSIAN_USER_EMAIL, ATLASSIAN_API_TOKEN"
        )
    
    return JiraClient(site_name, user_email, api_token)


def main():
    """CLI interface for Jira tools"""
    parser = argparse.ArgumentParser(description='Jira Cloud API Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List projects
    list_projects = subparsers.add_parser('list-projects', help='List all projects')
    list_projects.add_argument('--search', help='Search term for filtering projects')
    
    # Get project
    get_project = subparsers.add_parser('get-project', help='Get project details')
    get_project.add_argument('project', help='Project key or ID')
    
    # Search issues
    search_issues = subparsers.add_parser('search-issues', help='Search for issues')
    search_issues.add_argument('--jql', help='JQL query string')
    search_issues.add_argument('--project', help='Project key or ID')
    search_issues.add_argument('--max-results', type=int, default=50, help='Max results')
    
    # Get issue
    get_issue = subparsers.add_parser('get-issue', help='Get issue details')
    get_issue.add_argument('issue', help='Issue key or ID')
    
    # Create issue
    create_issue = subparsers.add_parser('create-issue', help='Create a new issue')
    create_issue.add_argument('project', help='Project key or ID')
    create_issue.add_argument('summary', help='Issue summary')
    create_issue.add_argument('issue_type', help='Issue type (Bug, Story, Task)')
    create_issue.add_argument('--description', help='Issue description')
    create_issue.add_argument('--priority', help='Priority level')
    create_issue.add_argument('--assignee', help='Assignee account ID')
    
    # Add comment
    add_comment = subparsers.add_parser('add-comment', help='Add comment to issue')
    add_comment.add_argument('issue', help='Issue key or ID')
    add_comment.add_argument('body', help='Comment text')
    
    # Get dev info
    get_dev_info = subparsers.add_parser('get-dev-info', help='Get development info')
    get_dev_info.add_argument('issue', help='Issue key or ID')
    
    # List statuses
    list_statuses = subparsers.add_parser('list-statuses', help='List project statuses')
    list_statuses.add_argument('project', help='Project key or ID')

    # Get transitions
    get_transitions = subparsers.add_parser('get-transitions', help='Get available transitions')
    get_transitions.add_argument('issue', help='Issue key or ID')

    # Transition issue
    transition_issue = subparsers.add_parser('transition-issue', help='Transition issue to new status')
    transition_issue.add_argument('issue', help='Issue key or ID')
    transition_issue.add_argument('transition_id', help='Transition ID')

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        client = get_client_from_env()
        
        if args.command == 'list-projects':
            result = client.list_projects(args.search)
        elif args.command == 'get-project':
            result = client.get_project(args.project)
        elif args.command == 'search-issues':
            result = client.search_issues(args.jql, args.project, args.max_results)
        elif args.command == 'get-issue':
            result = client.get_issue(args.issue)
        elif args.command == 'create-issue':
            result = client.create_issue(
                args.project, args.summary, args.issue_type,
                args.description, args.priority, args.assignee
            )
        elif args.command == 'add-comment':
            result = client.add_comment(args.issue, args.body)
        elif args.command == 'get-dev-info':
            result = client.get_dev_info(args.issue)
        elif args.command == 'list-statuses':
            result = client.list_statuses(args.project)
        elif args.command == 'get-transitions':
            result = client.get_transitions(args.issue)
        elif args.command == 'transition-issue':
            client.transition_issue(args.issue, args.transition_id)
            result = {"status": "success", "message": f"Issue {args.issue} transitioned"}

        print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
