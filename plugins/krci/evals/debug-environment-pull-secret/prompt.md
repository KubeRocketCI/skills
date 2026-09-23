---
name: debug-environment-pull-secret
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a developer on a KubeRocketCI platform. `krci env get orders dev -o json` shows our project `orders-api` with `"status": "degraded"`, `"sync": "synced"`, version `2.3.1`, deployed 20 minutes ago. The same version 2.3.1 has been running fine in environment `qa` since yesterday. The pod events in the dev environment namespace:

```text
Warning  Failed   kubelet  Failed to pull image "registry.example.com/orders/orders-api:2.3.1": failed to authorize: failed to fetch oauth token: unexpected status: 401 Unauthorized
Warning  Failed   kubelet  Error: ErrImagePull
Normal   BackOff  kubelet  Back-off pulling image "registry.example.com/orders/orders-api:2.3.1"
Warning  Failed   kubelet  Error: ImagePullBackOff
```

What is wrong and who owns the fix? Answer from what I pasted, do not run anything.
