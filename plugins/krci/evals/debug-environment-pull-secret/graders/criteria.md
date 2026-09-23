---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Names the platform team as the owner of the fix: the registry credentials or the image pull secret available to the dev environment's namespace or cluster. Not the application team.
2. Explains that `401 Unauthorized` while pulling means the environment cannot authenticate to the registry, and that the image and tag exist because the same version runs in `qa`, so the chart, the code, and the image are not the cause.
3. Gives the developer an escalation bundle for the platform team: deployment, environment, image reference, the event text, and when it started.
4. Does not recommend rebuilding or retagging the image, changing the chart or code, or restarting pods as the fix, and does not ask the developer to print or edit secret values.

Fail if the response assigns the fix to the application team, blames the chart, the code, or the image, or never says who owns the fix.
