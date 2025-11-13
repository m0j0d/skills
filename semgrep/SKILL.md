---
name: semgrep
description: Static analysis security scanning with Semgrep
tags: [security, linting, SAST, vulnerability-detection]
created_from: mcp-server
version: 1.0.0
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

**Based on:** Official Semgrep MCP server (github.com/semgrep/mcp)

## Installation

1. **Install Semgrep:**
   ```bash
   pip install semgrep
   ```

2. **Verify installation:**
   ```bash
   semgrep --version
   ```

## Quick Start

### Scan a directory for security issues

```python
from semgrep_tools import scan_code, parse_findings

# Scan code
results = scan_code('../skills/playwright/scripts')

# Parse results
summary = parse_findings(results)

print(f"Status: {summary['status']}")
print(f"High: {summary['summary']['high']}")
print(f"Medium: {summary['summary']['medium']}")
print(f"Low: {summary['summary']['low']}")
```

### Scan with specific rulesets

```python
# Use custom rulesets
results = scan_code(
    target_path='../skills/jira/scripts',
    rules=['p/security-audit', 'p/secrets', 'p/python']
)
```

## Available Functions

### `scan_code(target_path, rules=None, timeout=300)`

Scan code for security vulnerabilities.

**Parameters:**
- `target_path` (str): Path to file or directory to scan
- `rules` (list, optional): Semgrep rulesets (default: ['p/security-audit', 'p/secrets'])
- `timeout` (int, optional): Max scan time in seconds (default: 300)

**Returns:** Dictionary with scan results

**Security features:**
- Path validation (prevents directory traversal)
- Command safety (no shell injection)
- Resource limits (timeout, size limits)
- Input validation

### `parse_findings(scan_results)`

Parse and categorize scan findings.

**Parameters:**
- `scan_results` (dict): Output from `scan_code()`

**Returns:**
```python
{
    'summary': {'high': 0, 'medium': 2, 'low': 5},
    'findings': [...],  # List of finding details
    'status': 'passed|failed',
    'total_findings': 7
}
```

**Status logic:**
- `passed`: Zero high-severity findings
- `failed`: One or more high-severity findings

### `get_available_rulesets()`

List commonly used Semgrep rulesets.

**Returns:** List of rulesets with descriptions

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
# Scan a directory
python scripts/semgrep_tools.py ../skills/playwright/scripts

# Output:
# Status: PASSED
# High:   0
# Medium: 1
# Low:    3
# Total:  4
```

## Security Considerations

This skill has been hardened against common attack vectors:

- ✅ **Command injection** - Uses subprocess with list args, never `shell=True`
- ✅ **Directory traversal** - Path validation and canonicalization
- ✅ **Resource exhaustion** - 5-minute timeout, 100MB size limit
- ✅ **Information disclosure** - Output sanitization for sensitive data
- ✅ **Input validation** - All inputs validated before processing

## Use Cases

1. **Pre-commit scanning** - Catch vulnerabilities before they're committed
2. **Portfolio security audit** - Scan all skills for security issues
3. **CI/CD integration** - Block insecure code from deployment
4. **Code review** - Identify security concerns in pull requests

## Example: Portfolio-Wide Scan

```python
import os
from semgrep_tools import scan_code, parse_findings

skills_dir = '../skills'
results_summary = {}

# Scan each skill
for skill in os.listdir(skills_dir):
    skill_path = os.path.join(skills_dir, skill, 'scripts')

    if os.path.isdir(skill_path):
        results = scan_code(skill_path)
        summary = parse_findings(results)
        results_summary[skill] = summary['summary']

# Report
for skill, summary in results_summary.items():
    if summary['high'] > 0:
        print(f"❌ {skill}: {summary['high']} high-severity issues")
    else:
        print(f"✅ {skill}: Passed")
```

## Limitations

- **Scan time**: Large codebases may take several minutes
- **False positives**: Some findings may be false positives (review manually)
- **Language support**: Best results with Python, JavaScript, TypeScript
- **Internet required**: Downloads rules from Semgrep registry on first use

## Troubleshooting

**"Semgrep not found"**
- Install: `pip install semgrep`
- Verify: `semgrep --version`

**Timeout errors**
- Increase timeout: `scan_code(path, timeout=600)`
- Reduce scan scope: Target specific subdirectories

**False positives**
- Review findings manually
- Use `.semgrepignore` file in project root
- Add inline comments: `# nosemgrep`

## Related Skills

- **dependency-scanner** - Scan dependencies for vulnerabilities (future)
- **security-dashboard** - Visualize security status (future)

## References

- Semgrep Docs: https://semgrep.dev/docs
- MCP Server: https://github.com/semgrep/mcp
- Rule Registry: https://semgrep.dev/explore
