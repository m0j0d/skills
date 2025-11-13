#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Slack Workspace Integration Tools"""
import os, sys, json, argparse
from typing import Optional, Dict, List
try: import requests
except ImportError: print("Install: pip install requests --break-system-packages"); sys.exit(1)

class SlackClient:
    def __init__(self, bot_token: str):
        self.headers = {"Authorization": f"Bearer {bot_token}", "Content-Type": "application/json"}
    
    def _req(self, method: str, endpoint: str, **kw):
        r = requests.request(method, f"https://slack.com/api/{endpoint}", headers=self.headers, **kw)
        r.raise_for_status(); data = r.json()
        if not data.get('ok'): raise Exception(data.get('error'))
        return data
    
    def list_channels(self, types: str = "public_channel,private_channel", limit: int = 100):
        return self._req('GET', 'conversations.list', params={'types': types, 'limit': limit})['channels']
    
    def get_channel_info(self, channel_id: str):
        return self._req('GET', 'conversations.info', params={'channel': channel_id})['channel']
    
    def post_message(self, channel_id: str, text: str, thread_ts: Optional[str] = None):
        payload = {'channel': channel_id, 'text': text}
        if thread_ts: payload['thread_ts'] = thread_ts
        return self._req('POST', 'chat.postMessage', json=payload)
    
    def get_channel_history(self, channel_id: str, limit: int = 100, oldest: Optional[str] = None):
        params = {'channel': channel_id, 'limit': limit}
        if oldest: params['oldest'] = oldest
        return self._req('GET', 'conversations.history', params=params)['messages']
    
    def add_reaction(self, channel_id: str, timestamp: str, reaction: str):
        return self._req('POST', 'reactions.add', json={'channel': channel_id, 'timestamp': timestamp, 'name': reaction})
    
    def list_users(self, limit: int = 100):
        return self._req('GET', 'users.list', params={'limit': limit})['members']
    
    def get_user_profile(self, user_id: str):
        return self._req('GET', 'users.info', params={'user': user_id})['user']
    
    def search_messages(self, query: str, count: int = 20):
        return self._req('GET', 'search.messages', params={'query': query, 'count': count})['messages']['matches']

def main():
    parser = argparse.ArgumentParser(description='Slack Tools')
    sub = parser.add_subparsers(dest='cmd')
    lc = sub.add_parser('list-channels'); lc.add_argument('--types', default="public_channel,private_channel")
    gi = sub.add_parser('get-channel'); gi.add_argument('channel_id')
    pm = sub.add_parser('post-message'); pm.add_argument('channel_id'); pm.add_argument('text'); pm.add_argument('--thread')
    gh = sub.add_parser('get-history'); gh.add_argument('channel_id'); gh.add_argument('--limit', type=int, default=100)
    ar = sub.add_parser('add-reaction'); ar.add_argument('channel_id'); ar.add_argument('timestamp'); ar.add_argument('reaction')
    lu = sub.add_parser('list-users')
    gu = sub.add_parser('get-user'); gu.add_argument('user_id')
    sm = sub.add_parser('search'); sm.add_argument('query')
    
    args = parser.parse_args()
    if not args.cmd: parser.print_help(); return
    
    token = os.environ.get('SLACK_BOT_TOKEN')
    if not token: raise ValueError("Missing SLACK_BOT_TOKEN")
    client = SlackClient(token)
    
    try:
        if args.cmd == 'list-channels': result = client.list_channels(args.types)
        elif args.cmd == 'get-channel': result = client.get_channel_info(args.channel_id)
        elif args.cmd == 'post-message': result = client.post_message(args.channel_id, args.text, args.thread)
        elif args.cmd == 'get-history': result = client.get_channel_history(args.channel_id, args.limit)
        elif args.cmd == 'add-reaction': result = client.add_reaction(args.channel_id, args.timestamp, args.reaction)
        elif args.cmd == 'list-users': result = client.list_users()
        elif args.cmd == 'get-user': result = client.get_user_profile(args.user_id)
        elif args.cmd == 'search': result = client.search_messages(args.query)
        print(json.dumps(result, indent=2))
    except Exception as e: print(f"Error: {e}", file=sys.stderr); sys.exit(1)

if __name__ == '__main__': main()
