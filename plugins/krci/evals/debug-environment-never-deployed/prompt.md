---
name: debug-environment-never-deployed
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a QA engineer on a KubeRocketCI platform. Before a test cycle I checked environment `qa` of deployment `shop` with `krci env get shop qa -o json`. Every one of its three projects looks like this one:

```json
{
  "name": "shop-api",
  "status": "missing",
  "sync": "outofsync",
  "version": "NaN",
  "imageTag": "NaN",
  "imageDigest": null,
  "ingressUrls": [],
  "argocdUrl": "/applications/shop-qa-shop-api",
  "deployedAt": null,
  "valuesOverride": false
}
```

The environment itself reports `"status": "created"` and trigger type `Manual`. Missing and OutOfSync everywhere looks bad to me. Is qa broken, and who has to fix it before I can start testing? Answer from what I pasted, do not run anything.
