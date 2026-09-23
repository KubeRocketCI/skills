# Security Policy

## What is in scope

Skills are instructions that a coding agent follows with the user's identity, against systems that deliver to production. Treat the following as security issues:

- a skill, script, or agent in this repository that leads an agent to change state without the user's confirmation,
- content that prints, stores, or transmits secret values or credentials,
- instructions that work around a `Forbidden` response or otherwise widen access,
- prompt injection: text in this repository that steers an agent toward something its user did not ask for,
- a script that executes untrusted input.

The safety gate and the contract that every skill must follow are described in [docs/architecture.md](docs/architecture.md).

## Reporting a Vulnerability

The KubeRocketCI team takes security issues very seriously. If you believe you have found a security vulnerability in this repository, let us know as soon as possible. We investigate all legitimate reports and do our best to fix the problem quickly.

Report any suspected vulnerability to [SupportEPMD-EDP@epam.com](mailto:SupportEPMD-EDP@epam.com). We respond within 48 hours. To help us understand the nature and extent of the issue, include as much of the following as possible:

- the path of the skill, script, or manifest involved,
- the host and model where you observed the behavior,
- the request that triggers it and what the agent did,
- step-by-step instructions to reproduce,
- the impact, including how an attacker could exploit it.

## Policy

- **Do not publicly disclose the details of a potential vulnerability without express written consent from us.** Users need time to update, and we need time to address the issue comprehensively.
- We aim to resolve security issues within 7 days of disclosure, depending on complexity.
- Once the issue is resolved, we publish a security advisory with the release that fixes it.

## For users of the skills

Skills run with your permissions. Install them only from this repository or a fork you trust, review what an installer copies, and keep the confirmation prompts of your agent host enabled for shell commands.

## Contact

For questions about this policy, write to [SupportEPMD-EDP@epam.com](mailto:SupportEPMD-EDP@epam.com).
