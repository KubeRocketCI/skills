---
name: trace-story-full-status
tags: [krci-trace-story]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a delivery manager on a KubeRocketCI platform. My engineering lead wants the implementation status of story SHOP-158 for tomorrow's status call: which of our projects picked it up, whether the code is merged, the first version it shipped in, and which environments are currently running that version or a later one. I opened the ticket and the development panel in Jira is empty, so I have no linked commits or merge requests to start from. We have several projects on the platform and I don't know which one, if any, touched this story. Walk me through exactly how you would find all of this, project by project, with the commands you would run. Do not run anything.
