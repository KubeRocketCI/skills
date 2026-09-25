---
name: debug-environment-deploy-history
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a DevOps engineer on a KubeRocketCI platform. Project `shop-api` in environment `qa` of deployment `shop` has been degraded since this morning. Before I escalate I need two facts for the report: when the last deploy to `qa` ran and which version it rolled out, and which version was deployed to `qa` before that one. The environment deploys automatically on every build and has a manual approval gate. Give me the exact krci or kubectl commands and say which fields answer each question. Do not run anything.
