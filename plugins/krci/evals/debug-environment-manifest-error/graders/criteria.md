---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Names the application team as the owner of the fix: the project's Helm chart in `deploy-templates/` or its values. Not the platform team.
2. Explains that sync `unknown` here comes from Argo CD failing to render the chart (`helm template` fails on `.Values.service.port`), so Argo CD did reach the cluster and this is not a connectivity or cluster registration problem.
3. Gives a next step in the chart or its values, such as a default for `service.port` or a guard in the template, that can be checked locally with `helm template` in `deploy-templates/`, followed by a new build and a deploy of the fixed version.
4. Does not recommend waiting for the platform team, restarting, rolling back, or syncing as the fix.

Fail if the response names the platform team as the owner, agrees with the lead that the platform is broken, or never says who owns the fix.
