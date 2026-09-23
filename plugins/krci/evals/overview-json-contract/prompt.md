---
name: overview-json-contract
tags: [krci-overview]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I script against the `krci` CLI of KubeRocketCI. Do not run anything, just give me the commands:

1. A jq one-liner that prints the names of all projects from `krci project list -o json`.
2. A jq one-liner that prints `name` and health `status` of every application in environment `qa` of deployment `payments` from `krci env get payments qa -o json`.
3. A shell guard that detects that the krci session is not authenticated before the script continues.
