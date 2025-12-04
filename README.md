# Skills for Claude Code

Lightweight Python skills for Claude Code that call APIs directly, avoiding MCP server overhead.

## Available Skills

**[→ View dashboard with validation scores](https://m0j0d.github.io/skills/)**

12 skills including GitHub, Slack, Jira, Playwright, Memory, and more.

---

## Quick Start

**New to skills?** Try **[sequential-thinking](sequential-thinking/)** first - no API keys needed.

---

## 🤔 Why Skills Over MCP Servers?

**If most MCP servers just wrap well-documented APIs, why run a separate server process?**

```
MCP:   Claude → JSON-RPC → MCP Server → REST API
Skill: Claude → Python Script → REST API
```

- ⚡ **87% less context** - Lazy loading vs all-tools-loaded
- 🚀 **Simpler architecture** - No JSON-RPC layer
- 🎯 **Direct control** - Edit and debug easily
- 🔧 **Zero infrastructure** - No server processes

**Hypothesis:** For individual developers with standard APIs, skills may be simpler.

**Read the analysis:** [WHY-SKILLS.md](WHY-SKILLS.md) | [30+ case studies →](SKILLS-VS-MCP-ANALYSIS.md)

---

## Installation

**Skills directory location:**
- **Linux/Mac:** `~/.claude/skills/`
- **Windows:** `%USERPROFILE%\.claude\skills\`
- Create the directory if it doesn't exist: `mkdir -p ~/.claude/skills`

**Quick start:**

```bash
# 1. Clone this repository to a temporary location
git clone https://github.com/m0j0d/skills.git /tmp/claude-skills

# 2. Copy desired skills to your Claude Code skills directory
cp -r /tmp/claude-skills/fetch ~/.claude/skills/
cp -r /tmp/claude-skills/memory ~/.claude/skills/
# ... add more as needed

# 3. Install dependencies (if skill requires them)
pip install -r ~/.claude/skills/fetch/requirements.txt  # example
```

**Configuration** (for skills that need API access):

```bash
# Set environment variables for credentials
export GITHUB_TOKEN="your-token-here"
export TWITTER_API_KEY="your-key-here"
```

See each skill's documentation for specific setup requirements.

---

## Help Shape This Project

**This project needs real-world feedback:**

- Does the skills approach solve a problem for you?
- Which skills would you actually use in your workflow?
- What's confusing or broken in the installation?
- Are there MCP servers you'd want as skills?

**Get involved:**
- Try a skill and share your experience
- [Report issues or suggestions](https://github.com/m0j0d/skills/issues)
- [Read the contribution guide](CONTRIBUTING.md)

**Status:** Early release - your feedback shapes what gets built next.
