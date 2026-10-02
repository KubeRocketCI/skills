---
name: overview-wait-for-run
tags: [krci-overview]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a developer on a KubeRocketCI platform. I merged pull request 57 into `main` of project `orders` two minutes ago, and `krci pipelinerun list --project orders --pr 57 --type build` shows the build run `build-orders-main-x7k2p` as `Running`. `orders` uses semver versioning.

I need a shell snippet for my release script that blocks until this run ends, stops the script if the build did not succeed, and prints the version this build produced. Use the krci CLI. Do not run anything.
