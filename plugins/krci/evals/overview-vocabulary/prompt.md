---
name: overview-vocabulary
tags: [krci-overview]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

My team delivers software with KubeRocketCI. In the portal, my deployment `payments` has an environment `qa` that looks unhealthy. I have kubectl access to the platform cluster.

Which Kubernetes resources represent that deployment and that environment, and in which namespace do the application pods of that environment run? Answer concisely: resource kinds, their names, and how the namespace name is formed.
