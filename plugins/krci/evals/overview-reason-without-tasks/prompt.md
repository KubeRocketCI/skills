---
name: overview-reason-without-tasks
tags: [krci-overview]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a developer on a KubeRocketCI platform. A script of mine reports why the newest build run of project `orders` failed: it runs `krci pipelinerun list --project orders --type build --reason -o json` and reads the failed task from `.tasks`. When `.tasks` is missing, it sleeps 30 seconds and asks again.

Last night the newest run was `Cancelled`, `.tasks` never appeared, and the script looped until morning. I do not want a blind retry limit: some finished runs do get their tasks a moment later, and a run that is still going gets them when it ends.

How can the script tell from the output of that command whether asking again makes sense, and what should it do in each case? Use the krci CLI. Do not run anything.
