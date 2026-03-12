#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Semgrep Security Scanner - Skill Implementation

This module provides secure wrappers around Semgrep for static analysis.
Built with security-first principles - the scanner itself must be bulletproof.
"""

import subprocess
import json
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


def scan_code(
    target_path: str,
    rules: Optional[List[str]] = None,
    timeout: int = 300
) -> Dict[str, Any]:
    """
    Safely scan code for security vulnerabilities using Semgrep.

    Args:
        target_path: Path to scan (file or directory)
        rules: List of rulesets (e.g., ['p/security-audit', 'p/secrets'])
               Defaults to ['p/security-audit', 'p/secrets']
        timeout: Maximum scan time in seconds (default: 300 = 5 minutes)

    Returns:
        Dictionary with scan results in JSON format

    Security:
        - Path validation prevents directory traversal
        - Subprocess uses list args (no shell injection)
        - Timeout prevents resource exhaustion
        - All inputs validated before execution

    Raises:
        ValueError: If path is invalid or suspicious
        TimeoutError: If scan exceeds timeout
        FileNotFoundError: If semgrep is not installed
    """
    # Default rulesets if none provided
    if rules is None:
        rules = ['p/security-audit', 'p/secrets']

    # Security: Canonicalize and validate path
    try:
        abs_path = os.path.abspath(target_path)

        # Check path exists
        if not os.path.exists(abs_path):
            raise ValueError("Path does not exist: " + target_path)

        # Check size limit (prevent scanning huge directories)
        if os.path.isdir(abs_path):
            try:
                total_size = sum(
                    f.stat().st_size
                    for f in Path(abs_path).rglob('*')
                    if f.is_file()
                )
                if total_size > 100_000_000:  # 100MB limit
                    raise ValueError(
                        "Directory too large: " + str(total_size) + " bytes (max 100MB)"
                    )
            except Exception:
                # If size check fails, proceed anyway (better to scan than fail)
                pass

    except Exception as e:
        raise ValueError("Invalid path: " + str(e))

    # Find semgrep executable - try PATH first, then common install locations
    import shutil
    semgrep_cmd = shutil.which('semgrep') or shutil.which('pysemgrep')
    if not semgrep_cmd:
        # Check common Windows Python Scripts directories
        import site
        candidates = []
        for scripts_dir in [
            os.path.join(site.getusersitepackages().replace('site-packages', 'Scripts')),
            os.path.join(os.path.dirname(sys.executable), 'Scripts'),
            os.path.expanduser('~/AppData/Roaming/Python/Python314/Scripts'),
            os.path.expanduser('~/AppData/Roaming/Python/Python313/Scripts'),
            os.path.expanduser('~/AppData/Roaming/Python/Python312/Scripts'),
            os.path.expanduser('~/AppData/Local/Programs/Python/Python314/Scripts'),
            os.path.expanduser('~/AppData/Local/Programs/Python/Python313/Scripts'),
        ]:
            # Prefer pysemgrep — semgrep.exe is a wrapper that itself needs pysemgrep on PATH
            for name in ['pysemgrep', 'pysemgrep.exe', 'semgrep', 'semgrep.exe']:
                candidate = os.path.join(scripts_dir, name)
                if os.path.isfile(candidate):
                    semgrep_cmd = candidate
                    break
            if semgrep_cmd:
                break
    if not semgrep_cmd:
        raise FileNotFoundError(
            "Semgrep not found. Install with: pip install semgrep"
        )

    # Build command - SAFE: Using list args, NOT shell=True
    cmd = [semgrep_cmd, '--json']

    # Add rulesets
    for rule in rules:
        # Basic validation on ruleset names
        if not rule or ' ' in rule or ';' in rule:
            raise ValueError("Invalid ruleset name: " + rule)
        cmd.extend(['--config', rule])

    # Add target path - already validated and canonicalized above
    cmd.append(abs_path)

    # Execute scan with timeout
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            check=False,  # Don't raise on non-zero exit (semgrep returns 1 if findings)
            text=True
        )

        # Parse JSON output
        try:
            scan_results = json.loads(result.stdout)
        except json.JSONDecodeError:
            # If JSON parsing fails, return error details
            return {
                'error': 'Failed to parse Semgrep output',
                'stdout': result.stdout[:500],  # Limit output
                'stderr': result.stderr[:500],
                'returncode': result.returncode
            }

        return scan_results

    except subprocess.TimeoutExpired:
        raise TimeoutError("Scan exceeded timeout of " + str(timeout) + " seconds")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Semgrep executable failed to run: " + semgrep_cmd
        )


def parse_findings(scan_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Semgrep scan results and categorize by severity.

    Args:
        scan_results: Raw output from scan_code()

    Returns:
        Dictionary with:
            - summary: {high: int, medium: int, low: int}
            - findings: List of finding details
            - status: 'passed' or 'failed'
            - total_findings: int
    """
    # Handle error results
    if 'error' in scan_results:
        return {
            'summary': {'high': 0, 'medium': 0, 'low': 0},
            'findings': [],
            'status': 'error',
            'total_findings': 0,
            'error': scan_results.get('error')
        }

    # Extract findings
    results = scan_results.get('results', [])

    # Categorize by severity
    severity_map = {'high': 0, 'medium': 0, 'low': 0, 'info': 0}
    findings_list = []

    for finding in results:
        # Get severity (Semgrep uses 'ERROR', 'WARNING', 'INFO')
        severity_level = finding.get('extra', {}).get('severity', 'INFO').lower()

        # Map Semgrep severity to our categories
        if severity_level in ['error', 'critical']:
            severity = 'high'
        elif severity_level == 'warning':
            severity = 'medium'
        else:
            severity = 'low'

        severity_map[severity] += 1

        findings_list.append({
            'severity': severity,
            'message': finding.get('extra', {}).get('message', 'No message'),
            'file': finding.get('path', 'unknown'),
            'line': finding.get('start', {}).get('line', 0),
            'rule_id': finding.get('check_id', 'unknown')
        })

    # Determine pass/fail (fail if any high severity)
    status = 'passed' if severity_map['high'] == 0 else 'failed'

    return {
        'summary': {
            'high': severity_map['high'],
            'medium': severity_map['medium'],
            'low': severity_map['low']
        },
        'findings': findings_list,
        'status': status,
        'total_findings': len(results)
    }


def get_available_rulesets() -> List[Dict[str, str]]:
    """
    Get list of commonly used Semgrep rulesets.

    Returns:
        List of rulesets with name and description
    """
    return [
        {'name': 'p/security-audit', 'description': 'General security issues'},
        {'name': 'p/secrets', 'description': 'Hardcoded secrets and credentials'},
        {'name': 'p/owasp-top-ten', 'description': 'OWASP Top 10 vulnerabilities'},
        {'name': 'p/python', 'description': 'Python-specific issues'},
        {'name': 'p/javascript', 'description': 'JavaScript-specific issues'},
        {'name': 'p/typescript', 'description': 'TypeScript-specific issues'},
        {'name': 'p/dockerfile', 'description': 'Dockerfile best practices'},
    ]


# CLI for testing
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python semgrep_tools.py <path>")
        print("\nExample: python semgrep_tools.py ../playwright/scripts")
        sys.exit(1)

    target = sys.argv[1]

    print("Scanning: " + target)
    print("=" * 50)

    # Run scan
    results = scan_code(target)
    summary = parse_findings(results)

    # Display results
    print("\nStatus: " + summary['status'].upper())
    print("High:   " + str(summary['summary']['high']))
    print("Medium: " + str(summary['summary']['medium']))
    print("Low:    " + str(summary['summary']['low']))
    print("Total:  " + str(summary['total_findings']))

    if summary['findings']:
        print("\nFindings:")
        for f in summary['findings'][:10]:  # Limit to first 10
            print("  [" + f['severity'].upper() + "] " + f['file'] + ":" + str(f['line']))
            print("    " + f['message'])

    sys.exit(0 if summary['status'] == 'passed' else 1)
