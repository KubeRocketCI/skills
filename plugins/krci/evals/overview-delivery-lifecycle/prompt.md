---
name: overview-delivery-lifecycle
tags: [krci-overview]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am the product owner of a team that delivers with KubeRocketCI 3.15 and tracks work in Jira. Story SHOP-142 was merged last week into project `orders`, which is delivered by deployment `shop` with environments `qa` and `prod`.

How do I find out which version contains SHOP-142 and whether it already runs in `qa` and `prod`? Will the platform write the build version back to the Jira ticket for me? Do not run anything, just tell me the steps and the commands.
