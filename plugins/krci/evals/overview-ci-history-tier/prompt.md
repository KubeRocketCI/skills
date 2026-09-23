---
name: overview-ci-history-tier
tags: [krci-overview]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

A developer on a KubeRocketCI platform asks: "my pull request pipeline for project `orders` failed yesterday evening, why?"

Both the `krci` CLI (authenticated) and `kubectl` (developer role in the platform namespace) are available. Which one do you query first for that run and its failure reason, and why? Give the first two commands you would run. Do not run anything.
