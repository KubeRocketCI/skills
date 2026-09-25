---
name: debug-environment-nan-version
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a QA engineer on a KubeRocketCI platform. Our DevOps engineer added environment `qa` to deployment `shop` yesterday. I want to start testing, but `krci env get shop qa -o json` shows this for our only project:

```json
{
  "name": "shop-api",
  "status": "healthy",
  "sync": "unknown",
  "version": "NaN",
  "imageTag": "NaN",
  "imageDigest": null,
  "ingressUrls": [],
  "argocdUrl": "/applications/shop-qa-shop-api",
  "deployedAt": null,
  "valuesOverride": false,
  "conditions": [
    {
      "type": "ComparisonError",
      "message": "Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = unable to resolve 'NaN' to a commit SHA",
      "lastTransitionTime": "2026-09-24T14:05:11Z"
    }
  ],
  "operation": null
}
```

The environment itself reports `"status": "created"` and trigger type `Manual`. A developer on my team says the build never tagged the repository and I should open a bug for the application team. Is he right? Who owns the fix, and what do I do next? Answer from what I pasted, do not run anything.
