# Skills vs MCP Servers: Technical Analysis

**Purpose:** Evaluate when Skills vs MCP Servers make sense for different integrations
**Context:** Analysis based on Anthropic docs, MCP spec, and community experience
**Date:** November 2025

---

## Executive Summary

After analyzing integration patterns, we find that **many MCP servers wrap well-documented APIs**. For individual developers using Claude Code, Skills may offer simpler architecture and better token efficiency. MCP remains valuable for cross-platform deployments and enterprise scenarios.

**Key insight:** Most integrations follow a simple pattern: authenticate → call REST API → format response. The question is whether this requires server infrastructure or can be done directly.

---

## Architecture Comparison

### Skills
- **Structure:** Markdown + YAML metadata + optional scripts
- **Context:** ~100 tokens metadata, details loaded on-demand
- **Platform:** Claude Code only (currently)
- **Execution:** Direct API calls (Python + requests)

### MCP Servers
- **Structure:** Server process + JSON-RPC protocol
- **Context:** All tool descriptions in every context
- **Platform:** Any MCP-compatible client
- **Execution:** Client → JSON-RPC → Server → API

---

## Key Differences

| Dimension | Skills | MCP |
|-----------|--------|-----|
| Token overhead | ~100 tokens/skill | ~800 tokens/server |
| Customization | Edit files directly | Rebuild required |
| Distribution | Git, manual | npm/pip packages |
| Cross-platform | No | Yes |
| Infrastructure | None | Server process |

---

## Token Efficiency

**Scenario:** 5 integrations (Jira, GitHub, Slack, Notion, Database)

**MCP:**
```
5 servers × ~800 tokens = ~4,000 tokens baseline
(always loaded, whether used or not)
```

**Skills:**
```
5 skills × ~100 tokens = ~500 tokens baseline
(details loaded only when needed)
```

**Difference: ~87% reduction in baseline context**

---

## Integration Analysis: 30 Examples

Analysis assumes no prior knowledge of any implementations. Evaluating based on API characteristics and use case patterns.

### 🟢 Strong Case for Skills

These integrations have well-documented REST APIs, simple auth, and stateless operations:

#### **1. Atlassian Jira**
- **API:** REST API v3, comprehensive documentation
- **Auth:** Email + API token
- **Operations:** Search issues, create/update, JQL queries
- **Assessment:** ✅ **SKILL** - Straightforward REST, no complexity
- **Notes:** Stateless CRUD operations, well-documented

#### **2. TeamCity (JetBrains)**
- **API:** REST API with full documentation
- **Auth:** Bearer token
- **Operations:** Trigger builds, check status, fetch logs
- **Assessment:** ✅ **SKILL** - Simple CI/CD operations
- **Notes:** Atomic operations, no persistent state needed

#### **3. Linear**
- **API:** GraphQL with excellent docs
- **Auth:** API key
- **Operations:** Issues, projects, cycles
- **Assessment:** ✅ **SKILL** - Clean GraphQL API
- **Notes:** Similar to Jira, well-suited for direct calls

#### **4. Notion**
- **API:** REST API v1
- **Auth:** Integration token
- **Operations:** Query databases, create pages, update blocks
- **Assessment:** ✅ **SKILL** - Standard REST patterns
- **Notes:** Well-documented, stateless

#### **5. Stripe**
- **API:** REST API (legendary documentation)
- **Auth:** API key
- **Operations:** Customers, payments, subscriptions
- **Assessment:** ✅ **SKILL** - Official SDKs available
- **Notes:** Payment operations are stateless

#### **6. Airtable**
- **API:** REST API with clear docs
- **Auth:** API key or OAuth
- **Operations:** Records, tables, bases
- **Assessment:** ✅ **SKILL** - Straightforward CRUD
- **Notes:** Well-documented spreadsheet/database API

#### **7. Sentry**
- **API:** REST API
- **Auth:** Auth token
- **Operations:** Projects, issues, events, releases
- **Assessment:** ✅ **SKILL** - Error tracking queries
- **Notes:** Read-heavy operations, simple auth

#### **8. HubSpot**
- **API:** REST API with SDKs
- **Auth:** API key or OAuth
- **Operations:** Contacts, deals, tickets
- **Assessment:** ✅ **SKILL** - Standard CRM operations
- **Notes:** Well-documented REST endpoints

#### **9. Todoist**
- **API:** REST API v2
- **Auth:** Bearer token
- **Operations:** Tasks, projects, labels
- **Assessment:** ✅ **SKILL** - Simple task management
- **Notes:** Perfect for personal productivity automation

#### **10. Twitter/X**
- **API:** REST API v2
- **Auth:** OAuth 2.0 or Bearer token
- **Operations:** Tweets, users, searches
- **Assessment:** ✅ **SKILL** - Standard social API
- **Notes:** Well-documented despite platform changes

---

### 🔧 Local Tools (Obvious Skills)

These require no external API—just local operations:

#### **11. Git**
- **API:** Git CLI commands
- **Auth:** N/A (local)
- **Operations:** Status, diff, commit, push
- **Assessment:** ✅ **SKILL** - Local CLI wrapper
- **Notes:** Running server for `git` commands is overkill

#### **12. Filesystem**
- **API:** OS file operations
- **Auth:** N/A (local)
- **Operations:** Read, write, list, delete
- **Assessment:** ✅ **SKILL** - Basic file I/O
- **Notes:** No justification for server process

#### **13. Docker**
- **API:** Docker CLI + Docker Engine API
- **Auth:** Local socket or API key
- **Operations:** Containers, images, networks
- **Assessment:** ✅ **SKILL** - CLI wrapper is sufficient
- **Notes:** Most operations are local commands

#### **14. Sequential Thinking**
- **API:** None (state management)
- **Auth:** N/A
- **Operations:** Track thought sequences
- **Assessment:** ✅ **SKILL** - Pure local state
- **Notes:** No external dependencies

#### **15. Memory (Knowledge Graph)**
- **API:** None (local JSONL storage)
- **Auth:** N/A
- **Operations:** Store entities, relations
- **Assessment:** ✅ **SKILL** - Local file storage
- **Notes:** Personal context should stay local

#### **16. Time/Timezone**
- **API:** Python datetime/pytz
- **Auth:** N/A
- **Operations:** Convert times, format dates
- **Assessment:** ✅ **SKILL** - Standard library
- **Notes:** Server for timezone math is absurd

---

### 🌐 Web Utilities

#### **17. Fetch (Web Content)**
- **API:** HTTP + HTML parsing
- **Auth:** None (public web)
- **Operations:** GET requests, HTML→Markdown
- **Assessment:** ✅ **SKILL** - Simple HTTP + parsing
- **Notes:** requests + BeautifulSoup is standard

#### **18. Playwright**
- **API:** Playwright library (Python/Node)
- **Auth:** N/A (local browsers)
- **Operations:** Navigate, screenshot, interact
- **Assessment:** ✅ **SKILL** - Library wrapper
- **Notes:** MCP adds unnecessary layer over library

#### **19. Puppeteer/Selenium**
- **API:** Browser automation libraries
- **Auth:** N/A (local)
- **Operations:** Browser control, testing
- **Assessment:** ✅ **SKILL** - Similar to Playwright
- **Notes:** Direct library usage is simpler

---

### ⚖️ Context-Dependent

These could go either way depending on requirements:

#### **20. GitHub**
- **API:** REST + GraphQL (excellent docs)
- **Auth:** PAT or OAuth
- **Operations:** Repos, issues, PRs, actions
- **Assessment:** ⚖️ **DEPENDS**
  - **Skill:** Personal use, single repos
  - **MCP:** Enterprise org-wide deployment
- **Notes:** API is well-documented either way

#### **21. Slack**
- **API:** REST API + Real-time API (WebSocket)
- **Auth:** Bot token or OAuth
- **Operations:** Messages, channels, users
- **Assessment:** ⚖️ **DEPENDS**
  - **Skill:** Bot operations, automation
  - **MCP:** Real-time event handling
- **Notes:** WebSocket for events might favor MCP

#### **22. Discord**
- **API:** REST + Gateway (WebSocket)
- **Auth:** Bot token
- **Operations:** Messages, guilds, reactions
- **Assessment:** ⚖️ **DEPENDS**
  - **Skill:** Bot dev, testing
  - **MCP:** Production 24/7 bots
- **Notes:** Discord.py excellent for skills

#### **23. Gmail (Google Workspace)**
- **API:** Gmail API
- **Auth:** OAuth 2.0
- **Operations:** Read, send, search emails
- **Assessment:** ⚖️ **DEPENDS**
  - **Skill:** Personal email automation
  - **MCP:** Organization-wide shared accounts
- **Notes:** OAuth complexity same either way

#### **24. Google Drive**
- **API:** Drive API v3
- **Auth:** OAuth 2.0
- **Operations:** Files, folders, sharing
- **Assessment:** ⚖️ **DEPENDS**
- **Notes:** Similar to Gmail—depends on scale

#### **25. Google Calendar**
- **API:** Calendar API v3
- **Auth:** OAuth 2.0
- **Operations:** Events, calendars, availability
- **Assessment:** ⚖️ **DEPENDS**
- **Notes:** Personal productivity: skill works fine

#### **26. PostgreSQL / MySQL**
- **API:** Database protocol
- **Auth:** Username + password
- **Operations:** SQL queries, transactions
- **Assessment:** ⚖️ **DEPENDS** (slight MCP lean)
  - **MCP:** Connection pooling for production
  - **Skill:** Local dev databases, SQLite
- **Notes:** One case where persistent connections help

#### **27. Supabase**
- **API:** REST + Real-time subscriptions
- **Auth:** JWT, API keys
- **Operations:** Database, auth, storage
- **Assessment:** ⚖️ **DEPENDS**
  - **MCP:** Real-time subscriptions
  - **Skill:** Standard CRUD
- **Notes:** Real-time features favor MCP slightly

---

### 🎨 Developer Tools (Personal Dev Focus)

#### **28. Figma**
- **API:** REST API
- **Auth:** Personal access token
- **Operations:** Files, projects, comments, inspect designs
- **Assessment:** ✅ **SKILL** - Design inspection for dev
- **Notes:** Great for personal workflows, extract specs

#### **29. Vercel**
- **API:** REST API v2
- **Auth:** Bearer token
- **Operations:** Deployments, projects, domains, logs
- **Assessment:** ✅ **SKILL** - Deployment management
- **Notes:** Simple REST, perfect for personal projects

#### **30. Netlify**
- **API:** REST API
- **Auth:** Personal access token
- **Operations:** Sites, deploys, forms, functions
- **Assessment:** ✅ **SKILL** - Similar to Vercel
- **Notes:** Straightforward deployment API

#### **31. Obsidian (via REST plugins)**
- **API:** Local REST API (plugins)
- **Auth:** API key
- **Operations:** Notes, links, search
- **Assessment:** ✅ **SKILL** - Personal knowledge management
- **Notes:** Local-first, perfect for skills

#### **32. VS Code (via CLI)**
- **API:** VS Code CLI
- **Auth:** N/A (local)
- **Operations:** Open files, run commands, manage extensions
- **Assessment:** ✅ **SKILL** - Local editor integration
- **Notes:** CLI wrapper for automation

#### **33. Postman API**
- **API:** REST API
- **Auth:** API key
- **Operations:** Collections, requests, environments
- **Assessment:** ✅ **SKILL** - API testing workflows
- **Notes:** Useful for API development automation

#### **34. npm/yarn**
- **API:** CLI commands + npm registry API
- **Auth:** Token (for publishing)
- **Operations:** Install, publish, search packages
- **Assessment:** ✅ **SKILL** - Package management
- **Notes:** CLI wrapper with occasional API calls

#### **35. OpenAI API**
- **API:** REST API
- **Auth:** API key
- **Operations:** Chat completions, embeddings, assistants
- **Assessment:** ✅ **SKILL** - AI automation
- **Notes:** Meta-programming: Claude calling GPT

#### **36. Anthropic API**
- **API:** REST API
- **Auth:** API key
- **Operations:** Messages, streaming, vision
- **Assessment:** ✅ **SKILL** - Meta workflows
- **Notes:** Claude calling Claude for specialized tasks

---

### 🔐 Security-Sensitive (Potential MCP Case)

#### **37. Bitwarden**
- **API:** CLI + Vault API
- **Auth:** Master password + 2FA
- **Operations:** Retrieve secrets, store credentials
- **Assessment:** ❓ **BORDERLINE**
- **Notes:** Security isolation argument weak (same machine)

#### **38. 1Password**
- **API:** CLI + Connect API
- **Auth:** Service account token
- **Operations:** Items, vaults, secrets
- **Assessment:** ❓ **BORDERLINE**
- **Notes:** Similar to Bitwarden—minimal real isolation

---

## Decision Framework

### Choose Skills When:
1. Using Claude Code exclusively
2. API is well-documented (REST/GraphQL)
3. Auth is straightforward (keys, tokens)
4. Operations are stateless
5. Want rapid customization
6. Personal or small team use

### Choose MCP When:
1. Supporting multiple AI platforms
2. Enterprise deployment requirements
3. Need persistent connections (WebSockets, DB pools)
4. Formal team versioning needed
5. Central credential management required

### Consider Both When:
- Team uses various AI platforms
- Some users need simplicity, others need features
- Gradual migration from one to another

---

## Performance Estimates

**Latency per operation:**
- MCP: ~230ms (includes JSON-RPC overhead)
- Skill: ~202ms (direct API call)
- **Difference: ~12% faster**

**Context baseline (5 integrations):**
- MCP: ~4,000 tokens
- Skills: ~500 tokens
- **Difference: ~87% reduction**

---

## Security Reality Check

**Claim:** "MCP provides security isolation"

**Reality for localhost deployments:**
- Both run on same machine with same user permissions
- Credentials in env vars accessible to both
- No meaningful security boundary

**Reality for remote MCP servers:**
- Central credential management ✅ (real benefit)
- Network isolation ✅ (actual boundary)

**Verdict:** MCP wins only for true remote/enterprise deployments.

---

## Recommendations

### For Individual Developers
**Start with Skills** - Simpler, faster, easier to customize

### For Teams (2-10 people)
**Skills via Git** - Version control works fine for small teams

### For Organizations (10+ people)
**Consider MCP** - Central management becomes valuable

### For Multi-Platform
**MCP required** - Skills are Claude Code only (for now)

---

## This Repository's Experiments

This repo contains 12 experimental skill conversions from popular MCP servers:

| Skill | Source | Status |
|-------|--------|--------|
| fetch | modelcontextprotocol/servers (MIT) | Lightly tested |
| github | modelcontextprotocol/servers-archived (MIT, archived) | Experimental |
| github-actions | Custom (GitHub API docs) | Experimental |
| jira | Custom (Jira REST API v3) | Lightly tested |
| linear | jerhadf/linear-mcp-server (MIT, deprecated) | Experimental |
| memory | modelcontextprotocol/servers (MIT) | Lightly tested |
| notion | makenotion/notion-mcp-server (MIT) | Experimental |
| playwright | microsoft/playwright-mcp (Apache-2.0) | Lightly tested |
| semgrep | Custom (Semgrep wrapper) | Lightly tested |
| sequential-thinking | modelcontextprotocol/servers (MIT) | Lightly tested |
| slack | modelcontextprotocol/servers-archived (MIT, archived) | Experimental |
| twitter | crazyrabbitLTC/mcp-twitter-server (MIT) | Experimental |

**These are examples to test the conversion hypothesis—not validated implementations.**

---

## Conclusion

Many MCP servers wrap well-documented APIs that could be called directly. For individual developers using Claude Code, Skills may offer:
- Lower complexity (no server process)
- Better token efficiency (lazy loading)
- Faster iteration (edit files directly)

MCP remains valuable for:
- Cross-platform compatibility
- Enterprise deployments
- Persistent connections
- Formal team distribution

**The right choice depends on your constraints.**

---

## References

- **Anthropic Skills Docs:** https://docs.claude.com/en/docs/claude-code/skills
- **MCP Specification:** https://modelcontextprotocol.io
- **Skills vs MCP Analysis:** https://ericmjl.github.io/blog/2025/10/20/exploring-skills-vs-mcp-servers/
- **Simon Willison:** https://simonwillison.net/2025/Oct/16/claude-skills/

**Version:** 1.0
**Updated:** November 2025
