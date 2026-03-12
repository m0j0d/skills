---
name: semgrep
description: Static analysis security scanning with Semgrep
tags: [security, linting, SAST, vulnerability-detection]
created_from: mcp-server
version: 1.1.0
security:
  scan_status: passed
  scan_date: 2025-11-01
  semgrep_version: 1.142.0
  findings:
    high: 0
    medium: 0
    low: 0
  rules_used:
    - p/security-audit
    - p/secrets
---

# Semgrep Security Scanner

Static Application Security Testing (SAST) for finding vulnerabilities, detecting secrets, and enforcing code standards.

**Based on:** Semgrep MCP, integrated into the core `semgrep` binary as the `semgrep mcp` subcommand (supports stdio, streamable-http, and sse transports). See: https://semgrep.dev/docs/mcp

## Installation

1. **Install Semgrep:**
   ```bash
   pip install semgrep
   ```

2. **Verify installation:**
   ```bash
   semgrep --version
   ```

## Available Tools

### scan_code

Scan code for security vulnerabilities using Semgrep.

**Parameters:**
- `target_path` (str, required): Path to file or directory to scan
- `rules` (list[str], optional): Semgrep rulesets to use. Default: `["p/security-audit", "p/secrets"]`
- `timeout` (int, optional): Maximum scan time in seconds. Default: `300`

**Returns:** `dict` -- Raw Semgrep JSON output with `results` array, or error dict with `error`, `stdout`, `stderr`, `returncode` keys.

**Example:**
```python
from semgrep_tools import scan_code

results = scan_code("../skills/playwright/scripts")

results = scan_code(
    target_path="../skills/jira/scripts",
    rules=["p/security-audit", "p/secrets", "p/python"]
)
```

### parse_findings

Parse and categorize scan findings by severity.

**Parameters:**
- `scan_results` (dict, required): Raw output from `scan_code()`

**Returns:** `dict` with keys:
- `summary` (dict): `{high: int, medium: int, low: int}`
- `findings` (list[dict]): Each has `severity`, `message`, `file`, `line`, `rule_id`
- `status` (str): `"passed"` (zero high) or `"failed"` (one or more high)
- `total_findings` (int): Total count

**Example:**
```python
from semgrep_tools import scan_code, parse_findings

results = scan_code("../skills/playwright/scripts")
summary = parse_findings(results)
print(f"Status: {summary['status']}")
print(f"High: {summary['summary']['high']}")
print(f"Medium: {summary['summary']['medium']}")
print(f"Low: {summary['summary']['low']}")
```

### get_available_rulesets

List commonly used Semgrep rulesets.

**Parameters:** None

**Returns:** `list[dict]` -- Each dict has `name` (str) and `description` (str).

**Example:**
```python
from semgrep_tools import get_available_rulesets
for rs in get_available_rulesets():
    print(f"{rs['name']}: {rs['description']}")
```

## Common Rulesets

- `p/security-audit` - General security issues
- `p/secrets` - Hardcoded secrets and credentials
- `p/owasp-top-ten` - OWASP Top 10 vulnerabilities
- `p/python` - Python-specific issues
- `p/javascript` - JavaScript-specific issues
- `p/typescript` - TypeScript-specific issues
- `p/dockerfile` - Dockerfile best practices

## Command Line Usage

```bash
python scripts/semgrep_tools.py ../skills/playwright/scripts
```

## Security Considerations

- **Command injection** - Uses subprocess with list args, never shell=True
- **Directory traversal** - Path validation and canonicalization
- **Resource exhaustion** - 5-minute timeout, 100MB size limit
- **Input validation** - All inputs validated before processing

## Limitations

- **Scan time**: Large codebases may take several minutes
- **False positives**: Some findings may be false positives (review manually)
- **Language support**: Best results with Python, JavaScript, TypeScript
- **Internet required**: Downloads rules from Semgrep registry on first use

## References

- Semgrep Docs: https://semgrep.dev/docs
- MCP Server Docs: https://semgrep.dev/docs/mcp
- Rule Registry: https://semgrep.dev/explore
