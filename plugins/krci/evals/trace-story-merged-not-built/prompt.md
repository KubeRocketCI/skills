---
name: trace-story-merged-not-built
tags: [krci-trace-story]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a PM on a KubeRocketCI platform. Story SHOP-163 has a commit titled `SHOP-163: add proration to invoice totals` already merged into `main` in project `billing-api`, which uses semver versioning. `krci project deployments billing-api` doesn't show any environment on a version that looks like it was cut after the merge. Before I tell the lead this is stuck, how would you confirm, hands-on, that it really hasn't been built or deployed anywhere yet, and if it turns out nothing built, how would you find out whether a build even ran for that commit? Give me the exact commands. Do not run anything.
