# Skills for Claude Code

**Lightweight skills that call APIs directly, avoiding MCP context overhead.**

MCP servers are powerful, but running multiple servers (Jira, GitHub, Slack, etc.) can quickly fill your context window. This project explores an alternative: lightweight skills that call APIs directly, bypassing MCP entirely.

**What's here:**
- 12 skills (early development, seeking feedback)
- Security scanned with Semgrep
- Built from well-documented APIs

**How it works:**
Skills are generated from MCP server patterns, converted to direct API calls. Each skill is a Python script that Claude Code can invoke.

**Status:** Early release - seeking feedback on approach and real-world usage.

**Want to help?** Try a skill, report what works (or doesn't), suggest improvements. This approach needs validation from real users.

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

## What Are Skills?

Skills are Python-based extensions that give Claude Code access to external tools, APIs, and services. They're lightweight wrappers around well-documented APIs.

**Key benefits:**
- 🔒 **Secure** - No hardcoded secrets, environment variable based
- ✅ **Tested** - Automated validation with static analysis ([see reports](test-results/))
- 📚 **Documented** - Clear setup and usage instructions
- ⚡ **Efficient** - Lower token overhead than MCP servers

**Example:** The GitHub skill provides repository management, issues, PRs, and comments - everything the MCP server does, without running a separate process.

---

## The Generator Behind This

**These skills aren't hand-written - they're generated.**

We use a generator that converts MCP servers into skills through a systematic 4-step process: **Research** MCP capabilities → **Generate** Python wrappers → **Validate** with tests + security scans → **Document** setup and usage.

**How you can help now:**
- Try skills and report what works (or doesn't)
- Request skills you need - we prioritize based on demand
- Share use cases and workflows
- Suggest improvements to documentation

**What we're working toward:**
- Sharing the generator for creating skills
- Tools to help validate and test new skills
- A contributor pipeline for community-created skills

**Why progressive release?** The generator needs to work reliably before sharing it. We're actively developing this and will open-source the foundational pieces as they mature.

**The vision:** A community-runnable pipeline where anyone can contribute skills, validate them, and improve the generator.

---

## Getting Started

**New to Skills?** Try **[sequential-thinking](sequential-thinking/)** first - it demonstrates structured problem-solving without requiring API keys or external dependencies. Great for understanding how skills work.

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

## Available Skills

**[View the full dashboard with validation scores →](https://m0j0d.github.io/skills/)**

12 skills available, including GitHub, Slack, Jira, Playwright, and more. Each skill includes validation scores, security scans, and integration test results.

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
