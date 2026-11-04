---
name: debug-environment-pods-without-kubectl
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a QA engineer on a KubeRocketCI platform. I have a portal login and the krci CLI, but no kubectl and no access to the cluster. Project `cart-api` in environment `qa` of deployment `shop` has been degraded since this morning. `krci env get shop qa -o json` shows this, shortened:

```json
{
  "deployment": "shop",
  "env": "qa",
  "status": "created",
  "infrastructure": {
    "cluster": "in-cluster",
    "namespace": "krci-shop-qa",
    "triggerType": "Manual"
  },
  "projects": [
    {
      "name": "cart-api",
      "status": "degraded",
      "sync": "synced",
      "version": "1.4.2",
      "conditions": [],
      "operation": {
        "phase": "Succeeded",
        "message": "successfully synced (all tasks run)",
        "startedAt": "2026-11-03T07:58:12Z",
        "finishedAt": "2026-11-03T07:58:14Z"
      }
    }
  ]
}
```

Our DevOps engineer is on leave until Monday, and my lead says that without kubectl nobody on the team can see why the pods fail, so we should wait until they are back. Is that right? Which commands show me what is wrong with the pods? Do not run anything.
