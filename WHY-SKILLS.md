# Why Skills Instead of MCP Servers?

## The Question

**If most MCP servers just wrap well-documented APIs, why run a separate server process?**

```
MCP:   Claude → JSON-RPC → MCP Server → REST API
Skill: Claude → Python Script → REST API
```

---

## When Each Makes Sense

**Consider Skills when:**
- ✅ Using Claude Code exclusively
- ✅ API is well-documented (standard REST/GraphQL)
- ✅ Auth is straightforward (API keys, tokens)
- ✅ Want rapid customization and debugging

**Consider MCP when:**
- ✅ Supporting multiple AI platforms
- ✅ Enterprise deployment with central credentials
- ✅ Need persistent connections (WebSockets, DB pools)
- ✅ Require formal versioning across large teams

---

## This Repository

Contains **12 experimental skill conversions** from popular MCP servers. These are examples to explore whether the conversion pattern is viable—not proven production implementations.

**Hypothesis:** For individual developers using Claude Code with standard APIs, skills may offer lower complexity and better token efficiency.

**Status:** Early experimentation. Most skills untested in real workflows.

---

## Read The Analysis

Detailed comparison covering:
- Architecture and token efficiency
- 30+ integration case studies
- Security and performance considerations
- Decision framework

👉 **[Read the analysis →](SKILLS-VS-MCP-ANALYSIS.md)**

---

**Bottom line:** MCP is excellent for its intended use cases. Skills may be simpler for individual developers with standard APIs. Choose based on your constraints.
