# Contributing

## Ways to Contribute

### Report Bugs
Found something broken? [Open an issue](../../issues) with:
- What you expected vs. what happened
- Steps to reproduce
- Your environment (OS, Python version, Claude Code version)

### Request Skills or Improvements
Want a new skill or enhancement? [Open an issue](../../issues) with:
- Which API/service you want integrated and your use case
- What you want changed and why

### Submit Fixes
PRs are welcome for:
- Bug fixes in skill scripts
- Documentation improvements
- Test additions
- Security fixes

For larger changes (new skills, architectural changes), open an issue first to discuss.

---

## Development

### Skill Structure
Each skill follows a standard layout:
```
skill-name/
  SKILL.md          # Documentation, tools, examples
  scripts/
    skill_tools.py  # Implementation
  requirements.txt  # Dependencies (if any)
```

### Quality Checks
Skills are validated on three layers:
1. **Safety Gate** - security scan (no hardcoded secrets, no high-severity findings)
2. **Static Pre-flight** - syntax, imports, structure, type hints, error handling
3. **Behavioral Eval** - A/B test measuring skill value vs baseline

See the [dashboard](https://m0j0d.github.io/skills/) for current scores.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
