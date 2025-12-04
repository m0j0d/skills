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
