# Security Policy

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in any of the skills, please report it responsibly.

### Please DO NOT:
- ❌ Open a public GitHub issue for security vulnerabilities
- ❌ Post security issues in discussions or comments
- ❌ Disclose the vulnerability publicly before it's fixed

### Please DO:
- ✅ Report via GitHub Security Advisories
- ✅ Include detailed information about the vulnerability
- ✅ Provide steps to reproduce if possible
- ✅ Give us reasonable time to fix before public disclosure

## What to Report

### Security issues that should be reported:
- Hardcoded API keys, tokens, or passwords in code
- Ability to access files outside intended scope
- Command injection vulnerabilities
- Code execution vulnerabilities
- Exposure of sensitive user data
- Authentication or authorization bypass

### Issues that can be reported publicly:
- General bugs that don't expose sensitive data
- Documentation errors
- Feature requests
- Performance issues

## Our Approach

When you report a security issue, we strive to:

- Acknowledge receipt promptly
- Investigate and assess severity
- Develop and test fixes
- Coordinate responsible disclosure
- Credit reporters in release notes (if desired)

## Security Best Practices for Users

### When using skills:

**Environment Variables:**
- ✅ Store API keys in environment variables
- ✅ Never commit `.env` files to git
- ✅ Use different keys for development and production

**File Permissions:**
- ✅ Use filesystem skill with appropriate access controls
- ✅ Don't grant write access to sensitive directories
- ✅ Review file paths before executing

**API Keys:**
- ✅ Use least-privilege API keys (minimal permissions needed)
- ✅ Rotate keys regularly
- ✅ Revoke keys when no longer needed

**Code Review:**
- ✅ Review skill code before installing (it's open source!)
- ✅ Check for suspicious network requests
- ✅ Verify dependencies are from trusted sources

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| Older   | ❌ No              |

We only support the latest version of skills. Please update to the latest version before reporting issues.

## Security Approach

We aim to maintain security through:

- **Code review** - Manual review and validation scripts
- **Secret scanning** - Automated checks for hardcoded credentials
- **Minimal dependencies** - Trusted sources, regular updates
- **Safe design** - Configurable access controls, no arbitrary execution
- **Clear documentation** - Security guidelines and placeholder examples

## Known Limitations

### Current limitations users should be aware of:

**Filesystem Skill:**
- Access control is configuration-based (user must configure)
- No built-in sandboxing (relies on OS permissions)

**API Skills (twitter, github-actions, etc.):**
- API keys have full access to your accounts
- No rate limiting (relies on API provider limits)
- Errors may include API responses (don't log in production)

**Git Skill:**
- Can access any git repository on the system
- No restrictions on git operations

These are not vulnerabilities but design characteristics. Users should configure and use skills appropriately for their security requirements.

## Security Validation

We aim to validate skills through automated checks (secret scanning, syntax validation, dependency scanning), manual review, and community feedback.

## Vulnerability Disclosure

Security issues are handled on a best-effort basis. Response times vary based on severity, complexity, and maintainer availability. We aim for responsible disclosure coordinated with reporters.

## Past Security Issues

None reported yet (pre-launch).

When issues are fixed, we will document them here with:
- Brief description
- Severity level
- Fix version
- Credit to reporter (if permitted)

## Contact

**Security issues:** Use GitHub Security Advisories (see "Reporting a Vulnerability" above)

**General questions:** [Issues on GitHub](../../issues)

---

**Last updated:** 2025-09-20

Thank you for helping keep this project secure!
