---
name: debug-environment-sync-succeeded
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a developer on a KubeRocketCI platform. My merge to project `shop-api` was built an hour ago, and the platform deployed it automatically to environment `dev` of deployment `shop`. `krci env get shop dev -o json` now shows this for the project:

```json
{
  "name": "shop-api",
  "status": "degraded",
  "sync": "synced",
  "version": "main-20260924-101502",
  "imageTag": "main-20260924-101502",
  "imageDigest": null,
  "ingressUrls": [],
  "argocdUrl": "/applications/shop-dev-shop-api",
  "deployedAt": "2026-09-24T10:16:40Z",
  "valuesOverride": false,
  "conditions": [],
  "operation": {
    "phase": "Succeeded",
    "message": "successfully synced (all tasks run)",
    "startedAt": "2026-09-24T10:16:40Z",
    "finishedAt": "2026-09-24T10:16:40Z"
  }
}
```

Our release manager reads `"phase": "Succeeded"` as "the deploy to dev went through" and wants to promote this version to `qa` today. Did the deploy to `dev` succeed? Which krci command settles it, and where do I see the step that failed if it did not? I have no kubectl access. Do not run anything.
