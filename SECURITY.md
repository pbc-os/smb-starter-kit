# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in this repository, please email **security@prospectbutcher.co**.

We take security seriously and will respond within 48 hours.

## Scope

This repository contains documentation and scripts for AI agent skills. Please report issues related to:

- Accidentally committed secrets or credentials
- Insecure code patterns in scripts
- Documentation that encourages insecure practices
- Data exposure risks

## Out of Scope

- Third-party APIs documented in skills (report to those providers directly)
- Vulnerabilities in tools that skills integrate with (e.g., Slack, Google Ads)
- General questions about skill functionality

## Security Best Practices

All skills in this repository follow these principles:

1. **No hardcoded credentials** — All secrets use environment variables or secret managers
2. **Least privilege** — Skills document only the permissions they actually need
3. **Safe scripting** — Shell scripts use `set -uo pipefail` and proper quoting
4. **Clear warnings** — Sensitive operations (wallet management, API writes) include prominent security notices

## Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who report valid vulnerabilities (unless they prefer to remain anonymous).
