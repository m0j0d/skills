# Skills for Claude Code

Lightweight Python skills for Claude Code with direct API calls.

## Available Skills

**[View dashboard with scores and behavioral evals](https://m0j0d.github.io/skills/)**

12 skills: GitHub, Slack, Jira, Linear, Notion, Playwright, Semgrep, Memory, Sequential-thinking, Fetch, Twitter, GitHub Actions.

Each skill is scored on a 3-layer system:
- **Safety Gate** (pass/block) - security scan
- **Static Pre-flight** (/20) - structure, code quality, documentation
- **Behavioral Eval** (/80) - A/B test: does Claude do better WITH the skill?

---

## Quick Start

**New to skills?** Try **[sequential-thinking](sequential-thinking/)** first - no API keys needed.

```bash
# Clone to skills directory
# Linux/Mac: ~/.claude/skills
# Windows: %USERPROFILE%\.claude\skills
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

See each skill's SKILL.md for specific setup.

---

## Skills AND MCP Servers

Skills and MCP servers complement each other. Use what fits your workflow.

```
MCP:   Claude -> JSON-RPC -> MCP Server -> REST API
Skill: Claude -> Python Script -> REST API
```

**Skills** are simpler for personal automation, editable, no server process.
**MCP** is better for multi-platform support, teams, persistent connections.

**Read more:** [WHY-SKILLS.md](WHY-SKILLS.md)

---

## Feedback

[Share your experience or report issues](https://github.com/m0j0d/skills/issues).
