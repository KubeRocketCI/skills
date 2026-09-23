---
name: debug-environment-exact-syntax
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

A developer on a KubeRocketCI platform asks: "My `payments` deployment's `qa` environment looks
broken in the portal, but I want to check it from the terminal first. What's the exact command,
and which field in its output tells me whether it's actually unhealthy versus just out of sync
with Git?" Give the exact command and field names. Do not run anything.
