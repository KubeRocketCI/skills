---
name: debug-environment-manifest-error
tags: [krci-debug-environment]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

I am a developer on a KubeRocketCI platform. Environment `qa` of our deployment `payments` looks wrong, so I ran `krci env get payments qa -o json`. The part about our project:

```json
{
  "name": "payments-api",
  "status": "healthy",
  "sync": "unknown",
  "version": "1.4.0",
  "imageTag": "1.4.0",
  "imageDigest": "sha256:3f1c9a0d5be27e84c1f0a9d6e2b7c4a8d9e0f1a2b3c4d5e6f708192a3b4c5d6e",
  "ingressUrls": ["https://payments-api-qa.example.com"],
  "argocdUrl": "/applications/payments-qa-payments-api",
  "deployedAt": "2026-09-20T10:12:00Z",
  "valuesOverride": false
}
```

The Argo CD page of that Application shows this condition since we deployed 1.4.0 an hour ago:

```text
ComparisonError: Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = `helm template . --name-template payments-api --namespace platform-payments-qa --set image.tag=1.4.0 --include-crds` failed exit status 1: Error: template: payments-api/templates/deployment.yaml:42:28: executing "payments-api/templates/deployment.yaml" at <.Values.service.port>: nil pointer evaluating interface {}.port
```

My lead says `unknown` means the platform is broken and we should wait for the platform team. Is he right? Who owns the fix, and what is the next step? Answer from what I pasted, do not run anything.
