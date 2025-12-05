# Skills and MCP: Honest Trade-offs

**TL;DR:** Skills and MCP servers complement each other. Use what fits your workflow.

---

## The Core Question

**If an MCP server just wraps a well-documented API, do you need the server process?**

```
MCP:   Claude → JSON-RPC → MCP Server → REST API
Skill: Claude → Python Script → REST API
```

Both work. The right choice depends on your constraints.

---

## When Skills Make Sense

**✅ Choose Skills when:**
- Using Claude Code exclusively (skills are Claude Code only)
- API is well-documented (standard REST/GraphQL)
- Auth is straightforward (API keys, tokens in env vars)
- Want to edit/customize implementation directly
- Personal or small team use (2-5 people)
- Prefer simpler architecture (no server process)

**Examples that work well as skills:**
- GitHub/Jira/Linear (well-documented REST/GraphQL)
- Memory/Sequential-thinking (local state only)
- Fetch/Playwright (simple wrappers)
- Twitter/Slack basic operations (read/write)

---

## When MCP Makes Sense

**✅ Choose MCP when:**
- Supporting multiple AI platforms (not just Claude)
- Enterprise deployment requirements (formal versioning, central management)
- Need persistent connections (WebSockets, database pools)
- Team-wide distribution (10+ people)
- Require formal packaging/distribution (npm/pip)
- Compliance requires isolation (though both run on same machine for localhost)

**Examples that favor MCP:**
- Multi-platform tools used across different AI clients
- Production bots with 24/7 WebSocket connections
- Enterprise-wide integrations with central credential management
- Database connections with connection pooling

---

## What You Trade

### Skills Trade-offs

**Pros:**
- Simpler architecture (no server, no JSON-RPC)
- Edit files directly for customization/debugging
- Quality validation with transparent scores
- Zero infrastructure (just Python + pip)

**Cons:**
- Claude Code only (not portable to other platforms)
- Manual distribution (Git, copy files)
- No connection pooling/persistent state
- Less formal than packaged MCP servers

### MCP Trade-offs

**Pros:**
- Works across any MCP-compatible client
- Formal packaging/versioning (npm/pip)
- Persistent connections possible
- Better for team-wide distribution

**Cons:**
- Requires server process + JSON-RPC layer
- Harder to customize without rebuilding
- More infrastructure complexity

---

## Performance & Latency

**Latency:**
- Both add minimal overhead over direct API calls
- MCP: JSON-RPC layer (~few ms)
- Skills: Python import/execution (~few ms)
- Real bottleneck: The API call itself (100-500ms typically)

**Note:** Performance differences are negligible for typical use cases. Choose based on workflow fit, not performance.

---

## Security Reality

**Common misconception:** "MCP provides security isolation"

**Reality for localhost:**
- Both run on same machine with same user permissions
- Credentials typically in environment variables accessible to both
- No meaningful security boundary for local deployments

**Reality for remote MCP servers:**
- Central credential management ✅ (legitimate benefit)
- Network isolation ✅ (actual security boundary)

**Verdict:** MCP's security benefits only apply to remote/enterprise deployments, not localhost.

---

## Can You Use Both?

**Yes.** Use MCP for integrations that need it, skills for simpler cases.

Example setup:
- **MCP:** Database connections (connection pooling), multi-platform tools
- **Skills:** GitHub/Jira/Slack automation, local utilities (git, memory)

They're not mutually exclusive.

---

## This Repository

Contains **12 skill conversions** from popular MCP servers:

| Skill | Type | API Pattern |
|-------|------|-------------|
| fetch, memory, sequential-thinking, semgrep | Local/utility | No external API or simple wrapper |
| github, jira, linear, notion, slack, twitter | REST/GraphQL | Standard CRUD operations |
| github-actions | REST | CI/CD operations |
| playwright | Library wrapper | Browser automation |

**Status:** Experimental. Most are lightly tested in real workflows.

**Hypothesis:** For individual developers using Claude Code with standard APIs, skills may offer simpler architecture with less overhead.

---

## Decision Framework

Ask yourself:

1. **Platform:** Claude Code only? → Skills viable
2. **Team size:** Just you or small team? → Skills simpler
3. **API type:** Well-documented REST? → Either works
4. **Connections:** Need persistent state? → MCP has advantage
5. **Distribution:** Need formal packaging? → MCP better
6. **Customization:** Want to edit code directly? → Skills easier

**There's no universally "better" choice.** It depends on your constraints.

---

## The Honest Bottom Line

**MCP servers:**
- Anthropic's official protocol
- Excellent for cross-platform and enterprise use
- More infrastructure, but standardized

**Skills:**
- Simpler for individual developers with Claude Code
- Experimental approach (this repo is testing viability)
- Less infrastructure, but Claude Code only

**Both are valid.** Use what works for your situation. You can even use both together.

---

**This is an experiment:** We're testing whether the skill conversion pattern is viable for standard API wrappers. Early results suggest it works for many cases, but MCP remains the right choice for others.

**Feedback welcome:** [Report issues or share experience](https://github.com/m0j0d/skills/issues)
