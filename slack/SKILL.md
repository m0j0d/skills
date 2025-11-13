---
name: slack
description: Comprehensive Slack workspace integration for messaging, channel management, user interactions, and workspace automation
---

# Slack Workspace Integration

Full-featured Slack integration for workspace management and team communication.

**Based on:** Anthropic's archived MCP server (@modelcontextprotocol/servers-archived)

## When to Use

- Send and read messages
- Manage channels
- Search workspace content
- Get user information
- Add reactions
- Access message history

## Setup

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
pip install requests --break-system-packages
```

Create bot at api.slack.com/apps with scopes: channels:history, channels:read, chat:write, reactions:write, users:read

### Validation

After setup, validate your configuration:

```bash
# From project root
npm run validate:slack

# Or directly
python skills/slack/scripts/validate.py
```

The validation script checks:
- **Environment variables** - SLACK_BOT_TOKEN is set
- **Python dependencies** - Required libraries are installed
- **API connectivity** - Bot authentication and workspace access work

All checks must pass before using the skill.

## Key Tools

**list_channels** - List all channels
**post_message** - Send message to channel
**get_channel_history** - Read messages
**add_reaction** - Add emoji reaction
**list_users** - List workspace users
**get_user_profile** - Get user details
**search_messages** - Search workspace

## Example Usage

```bash
# List channels
python scripts/slack_tools.py list-channels

# Send message
python scripts/slack_tools.py post-message C0123456 "Hello team!"

# Get history
python scripts/slack_tools.py get-history C0123456 --limit 50

# Search messages
python scripts/slack_tools.py search "project alpha"
```

## Origin

Replicates korotovsky/slack-mcp-server and ubie-oss/slack-mcp-server functionality.
