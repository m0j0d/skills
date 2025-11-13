#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""GitHub Actions Workflow Management Tools"""

import os, sys, json, argparse
from typing import Optional, Dict, List
try:
    import requests
except ImportError:
    print("Install: pip install requests --break-system-packages"); sys.exit(1)

class GitHubActionsClient:
    def __init__(self, token: str):
        self.headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        self.base = "https://api.github.com"
    
    def _req(self, method: str, path: str, **kw) -> requests.Response:
        r = requests.request(method, f"{self.base}/{path.lstrip('/')}", headers=self.headers, **kw)
        r.raise_for_status(); return r
    
    def list_workflows(self, owner: str, repo: str) -> List[Dict]:
        return self._req('GET', f'repos/{owner}/{repo}/actions/workflows').json()['workflows']
    
    def get_workflow(self, owner: str, repo: str, workflow_id: str) -> Dict:
        return self._req('GET', f'repos/{owner}/{repo}/actions/workflows/{workflow_id}').json()
    
    def trigger_workflow(self, owner: str, repo: str, workflow_id: str, ref: str, inputs: Optional[Dict] = None) -> None:
        payload = {"ref": ref}
        if inputs: payload["inputs"] = inputs
        self._req('POST', f'repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches', json=payload)
    
    def list_workflow_runs(self, owner: str, repo: str, workflow_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        path = f'repos/{owner}/{repo}/actions/runs'
        params = {}
        if workflow_id: params['workflow_id'] = workflow_id
        if status: params['status'] = status
        return self._req('GET', path, params=params).json()['workflow_runs']
    
    def get_workflow_run(self, owner: str, repo: str, run_id: str) -> Dict:
        return self._req('GET', f'repos/{owner}/{repo}/actions/runs/{run_id}').json()
    
    def cancel_workflow_run(self, owner: str, repo: str, run_id: str) -> None:
        self._req('POST', f'repos/{owner}/{repo}/actions/runs/{run_id}/cancel')
    
    def rerun_workflow(self, owner: str, repo: str, run_id: str) -> None:
        self._req('POST', f'repos/{owner}/{repo}/actions/runs/{run_id}/rerun')
    
    def get_workflow_logs(self, owner: str, repo: str, run_id: str) -> bytes:
        return self._req('GET', f'repos/{owner}/{repo}/actions/runs/{run_id}/logs').content

def main():
    parser = argparse.ArgumentParser(description='GitHub Actions Tools')
    sub = parser.add_subparsers(dest='cmd')
    
    lw = sub.add_parser('list-workflows'); lw.add_argument('owner'); lw.add_argument('repo')
    gw = sub.add_parser('get-workflow'); gw.add_argument('owner'); gw.add_argument('repo'); gw.add_argument('workflow_id')
    tw = sub.add_parser('trigger'); tw.add_argument('owner'); tw.add_argument('repo'); tw.add_argument('workflow_id'); tw.add_argument('ref'); tw.add_argument('--inputs')
    lr = sub.add_parser('list-runs'); lr.add_argument('owner'); lr.add_argument('repo'); lr.add_argument('--workflow-id'); lr.add_argument('--status')
    gr = sub.add_parser('get-run'); gr.add_argument('owner'); gr.add_argument('repo'); gr.add_argument('run_id')
    cr = sub.add_parser('cancel'); cr.add_argument('owner'); cr.add_argument('repo'); cr.add_argument('run_id')
    rr = sub.add_parser('rerun'); rr.add_argument('owner'); rr.add_argument('repo'); rr.add_argument('run_id')
    gl = sub.add_parser('get-logs'); gl.add_argument('owner'); gl.add_argument('repo'); gl.add_argument('run_id')
    
    args = parser.parse_args()
    if not args.cmd: parser.print_help(); return
    
    token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
    if not token: raise ValueError("Missing GITHUB_PERSONAL_ACCESS_TOKEN")
    
    client = GitHubActionsClient(token)
    
    try:
        if args.cmd == 'list-workflows': result = client.list_workflows(args.owner, args.repo)
        elif args.cmd == 'get-workflow': result = client.get_workflow(args.owner, args.repo, args.workflow_id)
        elif args.cmd == 'trigger':
            inputs = json.loads(args.inputs) if args.inputs else None
            client.trigger_workflow(args.owner, args.repo, args.workflow_id, args.ref, inputs)
            result = {"status": "triggered"}
        elif args.cmd == 'list-runs': result = client.list_workflow_runs(args.owner, args.repo, args.workflow_id, args.status)
        elif args.cmd == 'get-run': result = client.get_workflow_run(args.owner, args.repo, args.run_id)
        elif args.cmd == 'cancel':
            client.cancel_workflow_run(args.owner, args.repo, args.run_id)
            result = {"status": "cancelled"}
        elif args.cmd == 'rerun':
            client.rerun_workflow(args.owner, args.repo, args.run_id)
            result = {"status": "rerunning"}
        elif args.cmd == 'get-logs':
            result = client.get_workflow_logs(args.owner, args.repo, args.run_id).decode('utf-8')
        
        print(result if isinstance(result, str) else json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)

if __name__ == '__main__':
    main()
