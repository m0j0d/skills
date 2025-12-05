# Skills for Claude Code

Lightweight Python skills for Claude Code with direct API calls - simple installation, quality validation.

## Available Skills

**[→ View dashboard with validation scores](https://m0j0d.github.io/skills/)**

12 skills including GitHub, Slack, Jira, Playwright, Memory, and more.

---

## Quick Start

**New to skills?** Try **[sequential-thinking](sequential-thinking/)** first - no API keys needed.

---

## 🤔 Skills AND MCP Servers: When to Use Each

**Skills and MCP servers complement each other** - use what fits your workflow.

```
MCP:   Claude → JSON-RPC → MCP Server → REST API
Skill: Claude → Python Script → REST API
```

**When to use skills:**
- 🚀 **Personal automation** - Quick setup for your own workflows
- 🎯 **Edit and debug** - Files you can modify directly
- 🔧 **No server process** - Just Python scripts
- 📊 **Quality validation** - Transparent scores and testing

**When to use MCP:**
- Multi-platform support (VS Code, other editors)
- Teams and enterprise (central credentials)
- Persistent connections (databases, WebSockets)

**Read more:** [WHY-SKILLS.md](WHY-SKILLS.md)

---

## Installation

```bash
# Clone to skills directory (Linux/Mac: ~/.claude/skills, Windows: %USERPROFILE%\.claude\skills)
git clone https://github.com/m0j0d/skills.git ~/.claude/skills

# Or copy individual skills
cp -r /path/to/skills/github ~/.claude/skills/

# Install dependencies if needed
pip install -r ~/.claude/skills/github/requirements.txt
```

**Configuration:** Skills that need API access use environment variables:

```bash
export GITHUB_TOKEN="your-token-here"
export SLACK_TOKEN="your-token-here"
```

See each skill's documentation for specific setup.

---

## Feedback Welcome

Early release - [share your experience or report issues](https://github.com/m0j0d/skills/issues).
